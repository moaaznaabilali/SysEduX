# SysEduX 🎛️

**SaaS Management System for Edux**

A comprehensive system to manage client subscriptions, monitor resource usage, and handle billing for the Edux SaaS platform.

## 🌟 Features

- **Client Management** - Register and manage clients
- **Subscription Plans** - 3 tiers: Basic, Professional, Enterprise
- **Resource Monitoring** - Track CPU, memory, storage per client
- **User Tracking** - Monitor user counts per instance
- **Billing & Invoicing** - Automated invoice generation
- **Access Control** - Hierarchical permissions (Viewer → Operator → Manager → Admin)
- **Health Checks** - Automated instance monitoring

## 📦 Modules

| Module | Description |
|--------|-------------|
| `sysedux_base` | Core module with subscription plans and access control |
| `sysedux_clients` | Client management and billing |
| `sysedux_monitoring` | Resource monitoring (Coming Soon) |

## 🚀 Installation

1. Clone this repository to your Odoo addons path
2. Update the apps list
3. Install `sysedux_base` (will install dependencies)

## 🔐 Access Levels

| Level | Permissions |
|-------|-------------|
| **Viewer** | Read-only access to active clients |
| **Operator** | Manage clients and subscriptions |
| **Manager** | Full management + billing + settings |
| **Administrator** | Full system access |

## 💰 Subscription Plans

| Plan | Users | Storage | Price/mo |
|------|-------|---------|----------|
| Basic | 10 | 5 GB | 500 SAR |
| Professional | 50 | 25 GB | 1,500 SAR |
| Enterprise | Unlimited | 100 GB | 5,000 SAR |

## 🔗 Links

- **Live System**: https://sysedux.dc-edux.com
- **Documentation**: Coming Soon
- **Support**: support@dc-edux.com

## 📄 License

LGPL-3

---

**DC-EDUX** © 2026
