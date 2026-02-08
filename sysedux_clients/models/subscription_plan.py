# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SubscriptionPlanClientExtension(models.Model):
    _inherit = 'sysedux.subscription.plan'

    # Relations - added here to avoid circular dependency
    client_ids = fields.One2many(
        'sysedux.client',
        'subscription_plan_id',
        string='Clients'
    )
    client_count = fields.Integer(
        string='Client Count',
        compute='_compute_client_count'
    )

    @api.depends('client_ids')
    def _compute_client_count(self):
        for plan in self:
            plan.client_count = len(plan.client_ids)
