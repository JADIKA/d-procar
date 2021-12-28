# -*- coding: utf-8 -*-
# from odoo import http


# class ProcarAccount(http.Controller):
#     @http.route('/procar_account/procar_account/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/procar_account/procar_account/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('procar_account.listing', {
#             'root': '/procar_account/procar_account',
#             'objects': http.request.env['procar_account.procar_account'].search([]),
#         })

#     @http.route('/procar_account/procar_account/objects/<model("procar_account.procar_account"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('procar_account.object', {
#             'object': obj
#         })
