from odoo.tests.common import TransactionCase
import json

class TestRecycleBin(TransactionCase):

    def setUp(self):
        super(TestRecycleBin, self).setUp()
        # Create test data
        self.user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'test_user',
            'email': 'test_user@example.com'
        })

        self.test_model = self.env['ir.model'].create({
            'name': 'Test Model',
            'model': 'test.model'
        })

        self.recycle_bin_record = self.env['recycle.bin'].create({
            'name': 'Test Record',
            'model_id': self.test_model.id,
            'record_id': 1,
            'deleted_data': json.dumps({
                'id': 1,
                'name': 'Test Data',
                'create_uid': self.user.id
            })
        })

    def test_restore_record(self):
        """Test restoring a record from the recycle bin"""
        recycle_bin = self.recycle_bin_record

        # Mock data to ensure restoration is possible
        self.env['test.model'] = self.env['ir.model']  # Replace with mock model if needed

        # Attempt restoration
        recycle_bin.restore_record()

        # Assert that the record was restored
        restored_record = self.env['test.model'].search([('id', '=', recycle_bin.record_id)])
        self.assertTrue(restored_record, "The record was not restored successfully.")
        self.assertEqual(restored_record.name, "Test Data", "Restored record data is incorrect.")

    def test_delete_old_records(self):
        """Test that old records are deleted after the lifecycle period"""
        recycle_bin = self.recycle_bin_record

        # Update the config parameter for lifecycle days
        self.env['ir.config_parameter'].sudo().set_param('recycle_bin.lifecycle_days', 1)

        # Simulate passage of time
        recycle_bin.write({'deleted_datetime': '2025-01-01 00:00:00'})
        self.env['recycle.bin'].delete_old_records()

        # Assert that the record was deleted
        remaining_records = self.env['recycle.bin'].search([('id', '=', recycle_bin.id)])
        self.assertFalse(remaining_records, "Old records were not deleted.")

    def test_unlink_behavior(self):
        """Test unlink behavior for extended BaseModel"""
        # Create a test record and delete it
        test_record = self.env['res.partner'].create({
            'name': 'Test Partner'
        })

        # Unlink the record and verify it goes to the recycle bin
        test_record.unlink()
        recycle_bin_entry = self.env['recycle.bin'].search([
            ('model_id', '=', self.env.ref('base.model_res_partner').id),
            ('record_id', '=', test_record.id)
        ])
        self.assertTrue(recycle_bin_entry, "The deleted record was not stored in the recycle bin.")
