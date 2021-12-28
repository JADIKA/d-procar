# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010, 2014 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import fields, api, models
from odoo.tools.translate import _


# TODO: Optimizar esto con sql
class all_etk(models.Model):
    _name = "all.etk"
    _description = "All ETK"
    
    sale_order_line_id = fields.Many2one('sale.order.line', _('Sale Order Line'), readonly=True)
    name = fields.Char(_('Name'), readonly=True)
    original = fields.Boolean(_('Original'), default=True, readonly=True)

    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now)
    pnr = fields.Char(_('Booking Reference'), copy=False)
    etk = fields.Char(_('Etk'), readonly=True)
    abaconet_id = fields.Char(_('Abaconet Invoice ID'), copy=False)
    customer = fields.Char(_('Customer'), readonly=True)

    price_total = fields.Float(string='Total Price', readonly=True,)
    price_cost_total = fields.Float(string='Total Cost', readonly=True,)
    total_taxes = fields.Float(string='Taxes', readonly=True)
    fare_basic = fields.Float(string='Fare Basic', readonly=True)    
    taxes_tx = fields.Float( string='Taxes Tx', readonly=True)
    services_fees = fields.Float( string='Services Fees', readonly=True)
    commission = fields.Float(string='Commission', readonly=True)

    _order = 'date_order asc'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        if view_type == 'tree':
            self.env.cr.execute('DELETE FROM all_etk WHERE id IN ( SELECT id FROM all_etk)')
            orders = self.env['sale.order'].search([])
            for order in orders:
                for order_line in order.order_line:
                    base_dict = {
                        'sale_order_line_id': order_line.id,
                        'name': order_line.product_id.name,
                        'date_order': order.date_order,
                        'pnr': order.pnr,
                        'etk': order_line.etk,
                        'customer': order_line.company_id.name,
                        'abaconet_id': order.abaconet_id,
                        'price_total': order_line.price_total,
                        'price_cost_total': order_line.price_cost_total,
                        'total_taxes': order_line.total_taxes,
                        'fare_basic': order_line.fare_basic,
                        'taxes_tx': order_line.taxes_tx,
                        'services_fees': order_line.services_fees,
                        'commission': order_line.commission    
                    }
                self.create(base_dict)
                
        return super(all_etk, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                             submenu=submenu)


    @api.multi
    def go_to_order(self):
        obj = self[0]
        return obj.sale_order_line_id.go_to_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
