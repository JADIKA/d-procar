# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class procar_purchase(models.Model):
#     _name = 'procar_purchase.procar_purchase'
#     _description = 'procar_purchase.procar_purchase'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
