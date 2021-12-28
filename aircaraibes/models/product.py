import datetime
from odoo import fields, models, api
from odoo.tools.translate import _

class product_template(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'


    commission_percent = fields.Integer(default=0, help="")
    service_fees = fields.Monetary(string='Service Fees', readonly=False)