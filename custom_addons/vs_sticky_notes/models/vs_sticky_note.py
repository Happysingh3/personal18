from odoo import models, fields

class NoteSticky(models.Model):
    _name = 'note.sticky'
    _description = 'Sticky Note'
    _order = 'id desc'

    name = fields.Char(string="Title", required=True)
    content = fields.Text(string="Content")
    color = fields.Char(string="Color", default="#fff9c4")

    res_model = fields.Char(string="Related Model", required=True)
    res_id = fields.Integer(string="Related Record ID", required=True)
    user_ids = fields.Many2many('res.users', string="Shared With")
    text_color = fields.Char(string="Color", default="#fff9c4")




