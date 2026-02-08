# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    sysedux_client_id = fields.Many2one(
        'sysedux.client',
        string='SysEduX Client',
        help='Link this invoice to a SysEduX client'
    )
