# -*- coding: utf-8 -*-
{
    'name': 'SysEduX Base',
    'version': '19.0.1.0.0',
    'category': 'SaaS Management',
    'summary': 'Core module for SysEduX SaaS Management System',
    'description': """
        SysEduX - SaaS Management System for Edux
        ==========================================
        
        Core Features:
        - Subscription Plans Management
        - Access Control & Hierarchy
        - Base Configuration
    """,
    'author': 'DC-EDUX',
    'website': 'https://dc-edux.com',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'account'],
    'data': [
        'security/sysedux_security.xml',
        'security/ir.model.access.csv',
        'data/subscription_plans.xml',
        'views/subscription_plan_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,
}
