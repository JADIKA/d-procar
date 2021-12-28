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

from odoo import api, fields, models, _
from odoo.exceptions import except_orm


class account_invoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    @api.model
    def create(self, vals):
        if not vals.get('date_invoice', False):
            order_obj = self.env['sale.order']
            order = order_obj.search([('name', '=', vals.get('origin', False))])
            vals['date_invoice'] = order and order.date_order or False
        inv_id = super(account_invoice, self).create(vals)
        self.generate_supplier_invoices(inv_id)
        return inv_id

    def get_other_invoices(self, ids):
        origin = self.read(ids, ['origin'])
        other_invoices = self.search([('origin', '=', origin),
                                               ('id', 'not in', ids)],)
        return other_invoices
    
    @api.multi
    def get_purchase_journal(self, company_id):
        journal = self.env['account.journal']
        jids = journal.search([('type', '=', 'purchase'),
                                        ('company_id', '=', company_id)])
        return jids and jids[0] or False

    def update_lines_by_supplier(self, lines_by_supplier, supplier, d):
        try:
            lines_by_supplier[supplier].append(d)
        except KeyError:
            lines_by_supplier[supplier] = [d]
        return lines_by_supplier

    def group_by_supplier(self, invoice):
        sol_obj = self.env['sale.order.line']
        sc_obj = self.env['sale.context']
        lines_by_supplier = {}
        for line in invoice.invoice_line:
            to_search = [('order_id.name', '=', line.origin),
                         ('product_id', '=', line.product_id.id)]
            sol_ids = sol_obj.search(to_search)
            if sol_ids:
                if len(sol_ids) > 1:
                    self._cr.execute('select order_line_id from \
                                sale_order_line_invoice_rel where \
                                invoice_id = %s', (line.id,))
                    sol_ids = self._cr.fetchall()[0]
                order_line = sol_obj.browse(sol_ids[0])
                try:
                    supplier = sc_obj.get_supplier(order_line)
                    data = {'invoice_line': line, 'sale_line': order_line}
                    self.update_lines_by_supplier(lines_by_supplier, supplier, data)
                except except_orm, excep:
                     raise excep

        return lines_by_supplier

    @api.multi
    def generate_supplier_invoices(self, inv_id):
        invoice = self.browse(inv_id)
        company_id = invoice.company_id
        journal_id = self.get_purchase_journal(company_id.id)
        vals = {
            'type': 'in_invoice',
            'state': 'draft',
            'journal_id': journal_id,
            'date_invoice': invoice.date_invoice,
            'period_id': invoice.period_id.id,
            'user_id': invoice.user_id.id,
            'company_id': company_id.id,
            'origin': invoice.origin,
            'comment': 'Generated from customer invoice ' + invoice.origin
        }

        lines_by_supplier = self.group_by_supplier(invoice)
        for s, lines in lines_by_supplier.items():
            currency_id = lines[0]['sale_line'].currency_cost_id.id
            data = vals.copy()
            data.update({
                'partner_id': s.id,
                'account_id': s.property_account_payable.id,
                'currency_id': currency_id,
                'invoice_line': []
            })
            for l in lines:
                sl = l['sale_line']
                il = l['invoice_line']
                cost_price = 0

                line_vals = {
                    'name': il.product_id.name,
                    'origin': il.invoice_id.number,
                    'product_id': il.product_id.id,
                    'account_id': il.product_id.categ_id.property_account_expense_categ.id,
                    'quantity': il.quantity,
                    'discount': il.discount,
                    'price_unit': cost_price
                }
                data['invoice_line'].append((0, 0, line_vals))
            inv_id = self.create(data)
