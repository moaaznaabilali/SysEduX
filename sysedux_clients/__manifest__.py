# -*- coding: utf-8 -*-
{
    'name': 'SysEduX Clients',
    'version': '19.0.1.0.0',
    'category': 'SaaS Management',
    'summary': 'Client Management for SysEduX',
    'description': """
        Client Management Module
        ========================
        
        Features:
        - Client registration and management
        - Subscription assignment
        - Instance configuration
        - User tracking per client
        - Invoice generation
    """,
    'author': 'DC-EDUX',
    'website': 'https://dc-edux.com',
    'license': 'LGPL-3',
    'depends': ['sysedux_base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/client_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
