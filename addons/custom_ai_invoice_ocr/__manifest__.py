{
    'name': 'Custom AI Invoice OCR',
    'version': '1.0',
    'summary': 'Extract text from invoice using OCR',
    'category': 'Accounting',
    'author': 'Your Company',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/ai_invoice_ocr_view.xml',
    ],
    'installable': True,
    'application': True,
}