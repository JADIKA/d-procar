# -*- coding: utf-8 -*-
{
    'name' : 'Custom Sales Report for Air Caraibes',
    'version' : '1.0',
    'summary': 'Custom report for the company sales',
    'sequence': 16,
    'category': 'Sales',
    'description': """
Custom Sales Report
=====================================
Air Caraibes report that will generate a pdf report for specific time duration.
    """,
    'category': 'Accounting',
    'website': '',
    'images' : [],
    'depends' : ['base_setup', 'report', 'sale'],
    'data': [
        'wizard/tkt_report_view.xml',
        'views/aircaraibes_report_report.xml',
        'views/layouts.xml',
        'views/report_tkt.xml'
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
