from odoo import models, fields, api
from odoo.tools.translate import _

class AccountMove(models.Model):
    _inherit = 'account.move'

    abaconet_id = fields.Char(_('Abaconet ID'), copy=False)
    
    date = fields.Date(string='Date', required=True, index=True, default=fields.Date.context_today)
    
        