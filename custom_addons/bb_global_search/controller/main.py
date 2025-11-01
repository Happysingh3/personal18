from odoo import http
from odoo.http import request

class CrmController(http.Controller):
    @http.route('/company/get_search_models', type='json', auth='user', methods=['GET','POST'])
    def get_company_search_models(self):
        return [{"name" : model_id.name,
                "model" : model_id.model}  for model_id in request.env.company.global_search_model_ids]