# -*- coding: utf-8 -*-


{
    'name': 'Wooden sale inhiret',
    'version': '1.0.0',
    'category': 'Wooden sale store',
    'summary': 'Wooden store',
    'description': """Wooden tools store""",
    'author': 'Dev',
    'depends': ['wooden_tools_store','sale','base','product'],
    'data': [
    # "security/ir.model.access.csv",
    "views/wooden_tools_view.xml",
    "views/sale_order_view.xml",




    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'License': 'LGPL-3',
    'application': True,
    'sequence': -98,

}
