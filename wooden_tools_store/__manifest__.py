# -*- coding: utf-8 -*-


{
    'name': 'Wooden tools store',
    'version': '1.0.0',
    'category': 'Wooden tools store',
    'summary': 'Wooden store',
    'description': """Wooden tools store""",
    'author': 'Dev',
    'depends': ['mail','product','report_xlsx','sale','stock','base','product'],
    'data': [
    "security/ir.model.access.csv",
    "data/sequnce_technical_view.xml",
    "wizard/cancel_order_wizard_veiw.xml",
    "views/menus.xml",
    "views/technical_order_view.xml",
    "report/report.xml",
    "report/technical_order_template.xml",
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'License': 'LGPL-3',
    'application': True,
    'sequence': -99,

}
