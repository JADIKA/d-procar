# -*- coding: utf-8 -*-
# from odoo import http


# class ProcarSale(http.Controller):
#     @http.route('/procar_sale/procar_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/procar_sale/procar_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('procar_sale.listing', {
#             'root': '/procar_sale/procar_sale',
#             'objects': http.request.env['procar_sale.procar_sale'].search([]),
#         })

#     @http.route('/procar_sale/procar_sale/objects/<model("procar_sale.procar_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('procar_sale.object', {
#             'object': obj
#         })
