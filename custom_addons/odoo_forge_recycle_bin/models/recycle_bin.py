from odoo import api, fields, models, _
import json
import logging
import base64
from datetime import datetime, timedelta


_logger = logging.getLogger(__name__)

class RecycleBin(models.Model):
    _name = 'recycle.bin'
    _description = 'Module to store deleted records'

    name = fields.Char(string='Name of Record', readonly=True)
    model_id = fields.Many2one('ir.model', readonly=True)
    record_id = fields.Integer('Deleted Record ID', readonly=True)
    parent_record_id = fields.Integer('Deleted Parent Record ID', readonly=True)
    deleted_datetime = fields.Datetime(string='Record Deleted at', readonly=True)
    user_id = fields.Many2one('res.users', "Deleted by", readonly=True)
    deleted_data = fields.Char('Record Data', readonly=False)  # in json
    parent_id = fields.Many2one('recycle.bin', string='Parent Record', readonly=True, help="Link to the parent record if this is a related record.")
    child_ids = fields.One2many('recycle.bin', 'parent_id', string='Related Records', readonly=True, help="Links to related records that were deleted with the parent record.")

    def restore_record(self):
        for record in self.filtered(lambda r: not r.parent_id):
            model_name = self.env['ir.model'].browse(record.model_id.id).model
            if model_name not in self.env:
                _logger.error(f"Model {model_name} does not exist. Skipping restoration.")
                continue
            data = json.loads(record.deleted_data)

            fields_info = self.env[model_name].fields_get()

            non_restorable_fields = ['id', 'create_date', 'write_date', '__last_update','image_1920','image_1024','image_256','image_512','commercial_partner_id']
            child_relationship_fields = [field for field, info in fields_info.items() if info['type'] in ('one2many', 'many2many')]

            # Combine lists of fields to exclude
            excluded_fields = set(non_restorable_fields + child_relationship_fields)

            # Remove excluded fields from the data
            for field in excluded_fields:
                data.pop(field, None)
            image_dict = {}
            # Adjust Many2one relational fields from [ID, "name"] to just ID
            for field_name, field_value in data.items():
                field_info = fields_info.get(field_name, {})
                if field_info.get('type') == 'datetime' and isinstance(field_value, str):
                    try:
                        parsed_datetime = datetime.strptime(field_value, "%Y-%m-%d %H:%M:%S.%f")
                        data[field_name] = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        # Handle cases where datetime conversion fails
                        _logger.error(f"Error parsing datetime for field {field_name} with value {field_value}")
                        parsed_datetime = datetime.strptime(field_value, "%Y-%m-%d %H:%M:%S")
                        data[field_name] = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(field_value, str) and field_value.startswith("b'") and field_value.endswith("'"):
                    # Ensure that the value is a string before performing string operations
                    image_data = field_value[2:-1]
                    data[field_name] = image_data
                elif isinstance(field_value, list) and len(field_value) == 2 and isinstance(field_value[0], int):
                    data[field_name] = field_value[0]

                
            _logger.info(f"Attempting to create {model_name} with cleaned data: {data}")

            # Create the record without child relationship fields
            new_record = self.env[model_name].create(data)
            new_record_id = new_record.id

            # Restore related records (e.g., sale.order.line)
            for child in record.child_ids:
                _logger.info(f"child: {child}")
                self.restore_child_record(child, new_record_id, record.record_id)

            self.get_related_records_data(parent_record_id=record.record_id, new_parent_record_id=new_record_id)

            record.unlink()

    def restore_child_record(self, child, new_order_id, original_order_id):
        _logger.info(f"restore_child_record STARTING")

        child_model_name = self.env['ir.model'].browse(child.model_id.id).model
        child_data = json.loads(child.deleted_data)
        
        # Update references and format Many2one fields
        for field_name, field_value in list(child_data.items()):
            # Check and replace specific record_id references with new_record_id
            if isinstance(field_value, list) and len(field_value) == 2:
                if field_value[0] == original_order_id:
                    _logger.warning(f"Replacing {original_order_id} with {new_order_id} on {field_name} - {field_value}")
                    child_data[field_name] = new_order_id  # Update with just the ID
                else:
                    # This ensures proper formatting for Many2one fields not being directly replaced
                    child_data[field_name] = field_value[0]  # Keep only the ID, discard the name
            elif field_value == original_order_id:
                # Direct integer match, uncommon but handled if necessary
                _logger.warning(f"Replacing {original_order_id} with {new_order_id} on {field_name} - {field_value}")
                child_data[field_name] = new_order_id

        # Exclude non-restorable fields
        excluded_fields = ['id', 'create_date', 'write_date', '__last_update']
        for field in excluded_fields:
            child_data.pop(field, None)

        _logger.info(f"Restoring {child_model_name} with corrected data: {child_data}")

        # Attempt to create the child record
        try:
            self.env[child_model_name].create(child_data)
        except Exception as e:
            _logger.error(f"Error restoring {child_model_name}: {e}", exc_info=True)

        child.unlink()


    def get_related_records_data(self, parent_record_id, new_parent_record_id):
        _logger.info(f"get_related_records_data STARTING with {parent_record_id} - {new_parent_record_id}")
        related_records = self.env['recycle.bin'].search([('parent_record_id', '=', parent_record_id)], order='record_id desc')

        if not related_records:
            _logger.warning("There are no related records...")
            return
        _logger.warning(f"related_records: {related_records}")

        for recycle_record in related_records:
            try:
                data = json.loads(recycle_record.deleted_data)
                model_name = recycle_record.model_id.model  
                model = self.env[model_name]

                prepared_data = {}
                for field_name, field_value in data.items():
                    _logger.warning(f"working on {field_name} with {field_value}")
                    field = model._fields.get(field_name)
                    _logger.warning(f"field: {field}")
                    
                    if field and field.type == 'many2one' and isinstance(field_value, list) and len(field_value) == 2:
                        prepared_data[field_name] = field_value[0]
                    elif field and field.type in ['one2many', 'many2many']:
                        continue
                    else:
                        prepared_data[field_name] = field_value

                # Correctly set 'res_id' if that's the intended logic
                # This condition was previously incorrect because it checked a non-existent key directly
                # and used the wrong condition to update 'res_id'
                if 'res_id' in prepared_data and prepared_data['res_id'] == parent_record_id:
                    prepared_data['res_id'] = new_parent_record_id

                # Exclude non-restorable fields
                excluded_fields = ['id', 'create_date', 'write_date', '__last_update']
                for field in excluded_fields:
                    prepared_data.pop(field, None)

                _logger.info(f"Restoring {model_name} with corrected data: {prepared_data}")
                new_related_record_id = self.env[model_name].create(prepared_data)
                _logger.warning(f"new_related_record_id: {new_related_record_id} for {model_name}")

            except json.JSONDecodeError as e:
                _logger.error(f"Error decoding JSON for recycle.bin record {recycle_record.id}: {e}")
                continue
            except Exception as e:
                _logger.error(f"Error restoring {model_name}: {e}", exc_info=True)

            recycle_record.unlink()


    def ensure_base64_encoded(self, data):
        """
        Ensure that the provided data is base64 encoded.
        If the data is not base64 encoded, encode it.
        """
        try:
            # If this step succeeds without raising an exception, the data is likely base64 encoded
            base64.b64decode(data, validate=True)
            _logger.warning(f"Trying to see if image is base64")
            return data  # Return the original data if it's already base64 encoded
        except Exception:
            # If an exception is raised, it means the data might not be base64 encoded
            _logger.warning(f"Encode the data into base64")
            return base64.b64encode(data.encode('utf-8')).decode('utf-8')

    @api.model
    def delete_old_records(self):
        lifecycle_days = int(self.env['ir.config_parameter'].sudo().get_param('recycle_bin.lifecycle_days', default=30))
        date_limit = fields.Datetime.now() - timedelta(days=lifecycle_days)
        old_records = self.search([('deleted_datetime', '<', date_limit)])
        old_records.unlink()
        _logger.info(f"Deleted {len(old_records)} records from the recycle bin older than {lifecycle_days} days.")

class BaseModelExtended(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def _get_model_id(self, model_name):
        return self.env['ir.model'].search([('model', '=', model_name)], limit=1).id

    def unlink(self):
        _logger.info(f"Unlink in BaseModelExtended class for {self._name} --- user id: {self.env.uid}")
        if self._name in ['recycle.bin', 'bus.bus','mail.message','mail.followers','ir.attachment','ir.model.data']:
            return super(BaseModelExtended, self).unlink()

        recycle_bin_env = self.env['recycle.bin']
        all_recycle_data = []
        try:
            related_records = self.related_one2many_field
            for related_record in related_records:
                _logger.warning(f"related_record: {related_record}")
        except Exception as e:
            pass

        # Step 1: Create recycle bin record for the main record first
        for record in self:
            _logger.warning(f"--------record: {record}")
            _logger.warning(f"record.read(): {record.read()}")
            if self._name == 'ir.attachment':
                # Custom handling for attachments before they are unlinked
                self._handle_attachments_before_unlink(record)
                continue
            record_data = record.read()[0]
            deleted_data = json.dumps(record_data, default=str)
            recycle_data_main = {
                'name': record.display_name or '',
                'model_id': self._get_model_id(self._name),
                'record_id': record.id,
                'deleted_datetime': fields.Datetime.now(),
                'user_id': self.env.uid,
                'deleted_data': deleted_data,
                # Initially, do not set parent_id for the main record
            }
            _logger.warning(f"recycle_data_main: {recycle_data_main}")
            if record_data.get("res_id"): 
                res_id_value = record_data.get('res_id', '')
                if ',' in str(res_id_value):
                    try:
                        _, res_id = res_id_value.split(',')
                        recycle_data_main['parent_record_id'] = int(res_id)  # Convert ID to integer
                    except ValueError:
                        _logger.error(f"Invalid res_id format for ir.property: {res_id_value}")
                        continue  
                else:

                    recycle_data_main['parent_record_id'] = res_id_value
            

            main_recycle_record = recycle_bin_env.create(recycle_data_main)
            all_recycle_data.append((record, main_recycle_record.id))

        # Step 2: Now handle related records and link them to the main record
        for record, parent_id in all_recycle_data:
            try:
                related_records = self._get_related_records_before_unlink()
            except Exception as e:
                _logger.error(f"Error fetching related records: {e}")
                related_records = []
            for related_record in related_records:
                related_record_data = related_record.read()[0]
                related_deleted_data = json.dumps(related_record_data, default=str)
                recycle_data_related = {
                    'name': related_record.display_name or '',
                    'model_id': self._get_model_id(related_record._name),
                    'record_id': related_record.id,
                    'deleted_datetime': fields.Datetime.now(),
                    'user_id': self.env.uid,
                    'deleted_data': related_deleted_data,
                    'parent_id': parent_id, 
                }
                recycle_bin_env.create(recycle_data_related)

        return super(BaseModelExtended, self).unlink()

    def _handle_attachments_before_unlink(self, attachment):
        _logger.info(f"Handling attachment {attachment.id} before unlinking.")

        recycle_bin_env = self.env['recycle.bin']
        attachment_data = attachment.read(fields=['name', 'res_model', 'res_id', 'type', 'url', 'mimetype'])[0]
        
        deleted_data = json.dumps(attachment_data, default=str)

        recycle_data = {
            'name': attachment_data.get('name', ''),
            'model_id': self._get_model_id('ir.attachment'),
            'record_id': attachment.id,  # Original attachment ID
            'deleted_datetime': fields.Datetime.now(),
            'user_id': self.env.uid,
            'deleted_data': deleted_data,
            'parent_record_id': attachment.res_id, 
        }

        recycle_bin_record = recycle_bin_env.create(recycle_data)
        _logger.info(f"Created recycle bin record for attachment {attachment.id} with recycle bin ID {recycle_bin_record.id}")


    def _get_related_records_before_unlink(self):
        related_records = []
        for record in self:
            if comodel_name not in self.env:
                _logger.error(f"Comodel {comodel_name} does not exist. Skipping.")
                continue
            for field in record._fields.values():
                if field.type == 'one2many':
                    comodel_name = field.comodel_name
                    comodel = self.env[comodel_name]
                    inverse_field_name = field.inverse_name
                    inverse_field = comodel._fields.get(inverse_field_name)

                    if isinstance(inverse_field, fields.Many2one) and inverse_field.ondelete == 'cascade':
                        related_records.extend(getattr(record, field.name).sudo())
        return related_records
