from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import AccessError, UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    abaconet_id = fields.Char(_('Abaconet ID'), copy=False)
    
 
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    abaconet_id = fields.Char(_('Abaconet ID'), copy=False)

