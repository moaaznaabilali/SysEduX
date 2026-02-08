# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SubscriptionPlan(models.Model):
    _name = 'sysedux.subscription.plan'
    _description = 'Subscription Plan'
    _order = 'sequence, id'

    name = fields.Char(
        string='Plan Name',
        required=True,
        translate=True
    )
    code = fields.Char(
        string='Plan Code',
        required=True,
        help='Unique identifier for the plan'
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10
    )
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    # Limits
    max_users = fields.Integer(
        string='Max Users',
        required=True,
        default=10,
        help='Maximum number of users allowed'
    )
    max_storage_gb = fields.Float(
        string='Max Storage (GB)',
        required=True,
        default=5.0,
        help='Maximum storage space in GB'
    )
    max_students = fields.Integer(
        string='Max Students',
        default=0,
        help='Maximum number of students (0 = unlimited)'
    )
    
    # Pricing
    price_monthly = fields.Monetary(
        string='Monthly Price',
        currency_field='currency_id',
        required=True
    )
    price_yearly = fields.Monetary(
        string='Yearly Price',
        currency_field='currency_id',
        compute='_compute_yearly_price',
        store=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    
    # Features
    features = fields.Text(
        string='Features',
        help='List of features included in this plan'
    )
    has_api_access = fields.Boolean(
        string='API Access',
        default=False
    )
    has_custom_domain = fields.Boolean(
        string='Custom Domain',
        default=False
    )
    has_priority_support = fields.Boolean(
        string='Priority Support',
        default=False
    )
    has_advanced_reports = fields.Boolean(
        string='Advanced Reports',
        default=False
    )
    
    # Relations
    client_ids = fields.One2many(
        'sysedux.client',
        'subscription_plan_id',
        string='Clients'
    )
    client_count = fields.Integer(
        string='Client Count',
        compute='_compute_client_count'
    )
    
    # Styling
    color = fields.Integer(
        string='Color Index'
    )
    badge_color = fields.Selection([
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('success', 'Success'),
        ('danger', 'Danger'),
        ('warning', 'Warning'),
        ('info', 'Info'),
    ], string='Badge Color', default='primary')

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Plan code must be unique!'),
    ]

    @api.depends('price_monthly')
    def _compute_yearly_price(self):
        """Calculate yearly price with 2 months free discount"""
        for plan in self:
            plan.price_yearly = plan.price_monthly * 10  # 2 months free

    @api.depends('client_ids')
    def _compute_client_count(self):
        for plan in self:
            plan.client_count = len(plan.client_ids)

    def name_get(self):
        result = []
        for plan in self:
            name = f"{plan.name} ({plan.max_users} users / {plan.max_storage_gb}GB)"
            result.append((plan.id, name))
        return result
