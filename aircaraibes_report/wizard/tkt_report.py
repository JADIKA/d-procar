# -*- coding: utf-8 -*-

from odoo import api, fields, models


class TktWizard(models.TransientModel):
    _name = "tkt.wizard"
    _description = "TKT wizard"

    date_from = fields.Datetime(string='Start Date')
    date_to = fields.Datetime(string='End Date')

    @api.multi
    def check_report(self):
        data = {}
        data['form'] = self.read(['date_from', 'date_to'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['date_from', 'date_to'])[0])
        return self.env['report'].get_action(self, 'aircaraibes_report.report_tkt', data=data)