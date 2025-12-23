from odoo import api, fields, models


class RestockKanbanConfig(models.Model):
    _name = 'restock.kanban.config'
    _description = 'Smart Restock Kanban Configuration'

    name = fields.Char('Name', default='Default Configuration')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
    )

    # Threshold settings (in days)
    healthy_threshold = fields.Integer(
        'Healthy Threshold (days)',
        default=30,
        help="Products with more than this many days of stock are considered healthy",
    )
    warning_threshold = fields.Integer(
        'Warning Threshold (days)',
        default=14,
        help="Products with stock between this and the healthy threshold are in warning status",
    )
    critical_threshold = fields.Integer(
        'Critical Threshold (days)',
        default=7,
        help="Products with stock between this and the warning threshold are in critical status",
    )

    # Calculation settings
    lookback_days = fields.Integer(
        'Lookback Period (days)',
        default=90,
        help="Number of days to analyze for average consumption calculation",
    )

    @api.model
    def get_config(self):
        """Get configuration for current company, creating one if it doesn't exist."""
        config = self.search([
            ('company_id', '=', self.env.company.id)
        ], limit=1)
        if not config:
            config = self.create({
                'name': f'{self.env.company.name} Configuration',
                'company_id': self.env.company.id,
            })
        return config
