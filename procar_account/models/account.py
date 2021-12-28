from odoo import models, fields, api

class AccountAccountType(models.Model):
    _inherit = "account.account.type"
    
    type = fields.Selection(selection_add=[('view','View')])