from odoo import http

class TestApi(http.Controller):
    @http.route('/test/api' , methods=["GET"], type='http' , auth='none' ,csrf=False)
    def test_endpoint(self):
        print("inside Test Api Method")