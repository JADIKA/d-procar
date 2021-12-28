from odoo import models, fields, api
from odoo.tools.translate import _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    abaconet_id = fields.Char(_('Abaconet ID'), copy=False)
    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    abaconet_id = fields.Char(_('Abaconet ID'), copy=False)