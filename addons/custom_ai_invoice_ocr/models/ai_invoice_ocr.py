from odoo import models, fields

class AiInvoiceOCR(models.Model):
    _name = 'ai.invoice.ocr'
    _description = 'AI Invoice OCR'

    name = fields.Char(string='Invoice Name', required=True)
    extracted_text = fields.Text(string='Extracted Text')