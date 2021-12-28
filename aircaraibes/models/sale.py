# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010, 2013, 2014 Tiny SPRL (<http://tiny.be>).
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

import time
import json as simplejson
import datetime as dt
from lxml import etree
from odoo import fields, api, models, exceptions
from odoo.models import TransientModel
from odoo.exceptions import except_orm
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools.translate import _
import odoo.addons.decimal_precision as dp


class sale_order(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'



    def get_today(self):
        return dt.date.today()


    
    abaconet_id = fields.Char(_('Abaconet Invoice ID'), copy=False)
    
    order_line = fields.One2many('sale.order.line', 'order_id', _('Order Lines'), readonly=True,
                                 states={'draft': [('readonly', False)],
                                         'sent': [('readonly', False)], 'editable': [('readonly', False)]
                                         })


class sale_order_line(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    @api.model
    def _default_services_fees(self):
        return line.product_id.service_fees
    
    @api.depends('product_id','price_unit','total_taxes')
    def _compute_f_basic(self):
        for line in self:
            f_basic = line.price_unit - line.total_taxes
            commission = f_basic * line.product_id.commission_percent / 100
            line.update({
                'fare_basic': f_basic,
                'commission': commission
            })

    @api.depends('product_id','price_unit','total_taxes','services_fees','commission')
    def _compute_amountInfo(self):
        """
        Compute the cost price of the SO line.
        """
        for line in self:
            taxes_tx = line.total_taxes - line.services_fees
            price_cost = line.price_unit - line.commission - line.services_fees
            line.update({
                'taxes_tx': taxes_tx,
                'purchase_price': price_cost
            })

    @api.depends('purchase_price','product_uom_qty')
    def _compute_costamount(self):
        """
        Compute the cost price of the SO line.
        """
        for line in self:
            price_cost = line.purchase_price * line.product_uom_qty
            line.update({
                'price_cost_total': price_cost
            })

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        f_basic = self.price_unit - self.total_taxes
        commission = f_basic * self.product_id.commission_percent / 100
        vals = {}
        vals['services_fees'] = self.product_id.service_fees
        vals['commission'] = commission
        self.update(vals)
        super(sale_order_line, self).product_id_change()

    etk = fields.Char(_('Ticket number'), copy=False, readonly=False)
    pnr = fields.Char(_('Booking Reference'), copy=False)
    form_of_payment = fields.Selection([
        ('ca', 'Cash'),
        ('cc', 'Credit Card'),
        ('ch', 'Check')
    ],_('Form of Payment'), required=True, default='ca')
    
    price_cost_total = fields.Monetary(compute='_compute_costamount', string='Total Cost', readonly=True, store=True)
    total_taxes = fields.Monetary(string='Taxes', readonly=False,required=True)
    fare_basic = fields.Monetary(compute='_compute_f_basic', string='Fare Basic', readonly=True, store=True)    
    taxes_tx = fields.Monetary(compute='_compute_amountInfo', string='Taxes Tx', readonly=True, store=True)
    services_fees = fields.Monetary(string='Services Fees', readonly=False, store=True)
    commission = fields.Monetary(string='Commission', readonly=False, store=True)
    supplier_id = fields.Many2one('res.partner', _('Supplier'), domain="[('supplier', '=', True)]")
