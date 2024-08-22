from odoo import http
from odoo.http import request

class MyController(http.Controller):
    @http.route('/my_api', type='json', auth='public')
    def my_api(self, **kwargs):
        return {'message': 'Hello, World!'}