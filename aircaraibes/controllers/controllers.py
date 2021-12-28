# -*- coding: utf-8 -*-
from odoo import http

# class Aircaraibes(http.Controller):
#     @http.route('/aircaraibes/aircaraibes/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aircaraibes/aircaraibes/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('aircaraibes.listing', {
#             'root': '/aircaraibes/aircaraibes',
#             'objects': http.request.env['aircaraibes.aircaraibes'].search([]),
#         })

#     @http.route('/aircaraibes/aircaraibes/objects/<model("aircaraibes.aircaraibes"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aircaraibes.object', {
#             'object': obj
#         })