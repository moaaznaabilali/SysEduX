# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta
import subprocess
import psutil
import logging

_logger = logging.getLogger(__name__)


class SyseduxClient(models.Model):
    _name = 'sysedux.client'
    _description = 'Client'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    # Basic Info
    name = fields.Char(
        string='Client Name',
        required=True,
        tracking=True
    )
    code = fields.Char(
        string='Client Code',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Contact',
        required=True,
        tracking=True
    )
    logo = fields.Binary(
        string='Logo'
    )
    
    # Instance Configuration
    domain = fields.Char(
        string='Subdomain',
        help='e.g., royal for royal.dc-edux.com',
        tracking=True
    )
    full_domain = fields.Char(
        string='Full Domain',
        compute='_compute_full_domain',
        store=True
    )
    db_name = fields.Char(
        string='Database Name',
        required=True,
        tracking=True
    )
    db_port = fields.Integer(
        string='Database Port',
        default=5432
    )
    instance_port = fields.Integer(
        string='Instance Port',
        required=True,
        tracking=True
    )
    server_ip = fields.Char(
        string='Server IP',
        default='157.173.123.122'
    )
    
    # Subscription
    subscription_plan_id = fields.Many2one(
        'sysedux.subscription.plan',
        string='Subscription Plan',
        required=True,
        tracking=True
    )
    status = fields.Selection([
        ('draft', 'Draft'),
        ('trial', 'Trial'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True)
    
    # Dates
    start_date = fields.Date(
        string='Start Date',
        default=fields.Date.today,
        tracking=True
    )
    trial_end_date = fields.Date(
        string='Trial End Date',
        compute='_compute_trial_end_date',
        store=True
    )
    next_billing_date = fields.Date(
        string='Next Billing Date',
        tracking=True
    )
    expiry_date = fields.Date(
        string='Expiry Date',
        tracking=True
    )
    
    # Usage Limits from Plan
    max_users = fields.Integer(
        string='Max Users',
        related='subscription_plan_id.max_users',
        store=True
    )
    max_storage_gb = fields.Float(
        string='Max Storage (GB)',
        related='subscription_plan_id.max_storage_gb',
        store=True
    )
    
    # Current Usage
    current_users = fields.Integer(
        string='Current Users',
        compute='_compute_current_usage',
        store=True
    )
    current_storage_gb = fields.Float(
        string='Current Storage (GB)',
        compute='_compute_current_usage',
        store=True
    )
    current_students = fields.Integer(
        string='Current Students',
        compute='_compute_current_usage',
        store=True
    )
    
    # Usage Percentages
    users_usage_percent = fields.Float(
        string='Users Usage %',
        compute='_compute_usage_percent'
    )
    storage_usage_percent = fields.Float(
        string='Storage Usage %',
        compute='_compute_usage_percent'
    )
    
    # Resource Monitoring
    cpu_usage = fields.Float(
        string='CPU Usage %'
    )
    memory_usage_mb = fields.Float(
        string='Memory Usage (MB)'
    )
    last_health_check = fields.Datetime(
        string='Last Health Check'
    )
    is_online = fields.Boolean(
        string='Online',
        compute='_compute_is_online'
    )
    
    # Billing
    monthly_price = fields.Monetary(
        string='Monthly Price',
        related='subscription_plan_id.price_monthly',
        store=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    invoice_ids = fields.One2many(
        'account.move',
        'sysedux_client_id',
        string='Invoices',
        domain=[('move_type', '=', 'out_invoice')]
    )
    invoice_count = fields.Integer(
        string='Invoice Count',
        compute='_compute_invoice_count'
    )
    total_invoiced = fields.Monetary(
        string='Total Invoiced',
        compute='_compute_invoice_totals',
        currency_field='currency_id'
    )
    total_paid = fields.Monetary(
        string='Total Paid',
        compute='_compute_invoice_totals',
        currency_field='currency_id'
    )
    balance_due = fields.Monetary(
        string='Balance Due',
        compute='_compute_invoice_totals',
        currency_field='currency_id'
    )
    
    # Notes
    notes = fields.Html(
        string='Internal Notes'
    )
    
    # Color for Kanban
    color = fields.Integer(
        string='Color Index'
    )

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Client code must be unique!'),
        ('db_name_unique', 'UNIQUE(db_name)', 'Database name must be unique!'),
        ('domain_unique', 'UNIQUE(domain)', 'Subdomain must be unique!'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', _('New')) == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code('sysedux.client') or _('New')
        return super().create(vals_list)

    @api.depends('domain')
    def _compute_full_domain(self):
        for client in self:
            if client.domain:
                client.full_domain = f"{client.domain}.dc-edux.com"
            else:
                client.full_domain = False

    @api.depends('start_date')
    def _compute_trial_end_date(self):
        for client in self:
            if client.start_date:
                client.trial_end_date = client.start_date + timedelta(days=14)
            else:
                client.trial_end_date = False

    def _compute_current_usage(self):
        """Fetch current usage from client database"""
        for client in self:
            try:
                # This will be implemented to query the client's database
                client.current_users = 0
                client.current_storage_gb = 0.0
                client.current_students = 0
            except Exception as e:
                _logger.warning(f"Failed to fetch usage for {client.name}: {e}")
                client.current_users = 0
                client.current_storage_gb = 0.0
                client.current_students = 0

    @api.depends('current_users', 'max_users', 'current_storage_gb', 'max_storage_gb')
    def _compute_usage_percent(self):
        for client in self:
            if client.max_users > 0:
                client.users_usage_percent = (client.current_users / client.max_users) * 100
            else:
                client.users_usage_percent = 0
            
            if client.max_storage_gb > 0:
                client.storage_usage_percent = (client.current_storage_gb / client.max_storage_gb) * 100
            else:
                client.storage_usage_percent = 0

    def _compute_is_online(self):
        """Check if instance is responding"""
        for client in self:
            if client.last_health_check:
                # Consider online if last check was within 5 minutes
                time_diff = datetime.now() - client.last_health_check
                client.is_online = time_diff.total_seconds() < 300
            else:
                client.is_online = False

    def _compute_invoice_count(self):
        for client in self:
            client.invoice_count = len(client.invoice_ids)

    def _compute_invoice_totals(self):
        for client in self:
            invoices = client.invoice_ids.filtered(lambda i: i.state == 'posted')
            client.total_invoiced = sum(invoices.mapped('amount_total'))
            client.total_paid = sum(invoices.mapped('amount_total')) - sum(invoices.mapped('amount_residual'))
            client.balance_due = sum(invoices.mapped('amount_residual'))

    # Actions
    def action_activate(self):
        """Activate client subscription"""
        self.ensure_one()
        self.write({
            'status': 'active',
            'next_billing_date': fields.Date.today() + timedelta(days=30),
        })
        self.message_post(body=_("Client activated."))

    def action_suspend(self):
        """Suspend client for non-payment or violation"""
        self.ensure_one()
        self.write({'status': 'suspended'})
        self.message_post(body=_("Client suspended."))

    def action_cancel(self):
        """Cancel client subscription"""
        self.ensure_one()
        self.write({'status': 'cancelled'})
        self.message_post(body=_("Client subscription cancelled."))

    def action_start_trial(self):
        """Start trial period"""
        self.ensure_one()
        self.write({
            'status': 'trial',
            'start_date': fields.Date.today(),
        })
        self.message_post(body=_("Trial period started for 14 days."))

    def action_view_invoices(self):
        """View client invoices"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoices'),
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('sysedux_client_id', '=', self.id), ('move_type', '=', 'out_invoice')],
            'context': {'default_sysedux_client_id': self.id, 'default_move_type': 'out_invoice'},
        }

    def action_create_invoice(self):
        """Create monthly invoice for client"""
        self.ensure_one()
        
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'sysedux_client_id': self.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'name': f"{self.subscription_plan_id.name} Subscription - {self.name}",
                'quantity': 1,
                'price_unit': self.monthly_price,
            })],
        }
        
        invoice = self.env['account.move'].create(invoice_vals)
        
        self.message_post(body=_("Invoice %s created.") % invoice.name)
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
        }

    def action_refresh_usage(self):
        """Manually refresh usage statistics"""
        self.ensure_one()
        self._compute_current_usage()
        self._check_health()
        self.message_post(body=_("Usage statistics refreshed."))

    def _check_health(self):
        """Check instance health"""
        self.ensure_one()
        try:
            # Simple port check
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.server_ip, self.instance_port))
            sock.close()
            
            self.write({
                'last_health_check': fields.Datetime.now(),
            })
            
            return result == 0
        except Exception as e:
            _logger.warning(f"Health check failed for {self.name}: {e}")
            return False

    @api.model
    def _cron_check_all_health(self):
        """Cron job to check health of all active clients"""
        clients = self.search([('status', 'in', ['active', 'trial'])])
        for client in clients:
            client._check_health()

    @api.model
    def _cron_refresh_all_usage(self):
        """Cron job to refresh usage statistics"""
        clients = self.search([('status', 'in', ['active', 'trial'])])
        for client in clients:
            client._compute_current_usage()
