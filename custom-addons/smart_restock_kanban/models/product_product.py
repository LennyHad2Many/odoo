from datetime import timedelta

from odoo import _, api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Computed fields for the Smart Restock Kanban board
    days_of_stock = fields.Float(
        'Days of Stock',
        compute='_compute_restock_metrics',
        store=True,
        digits=(12, 1),
        help="Projected days of stock remaining based on average daily consumption",
    )

    stock_status = fields.Selection([
        ('out_of_stock', 'Out of Stock'),
        ('critical', 'Critical'),
        ('warning', 'Warning'),
        ('healthy', 'Healthy'),
    ], string='Stock Status', compute='_compute_restock_metrics', store=True)

    stock_status_sequence = fields.Integer(
        'Status Sequence',
        compute='_compute_restock_metrics',
        store=True,
        help="Used for sorting: 1=Out of Stock, 2=Critical, 3=Warning, 4=Healthy",
    )

    avg_daily_consumption = fields.Float(
        'Avg. Daily Consumption',
        compute='_compute_restock_metrics',
        store=True,
        digits='Product Unit',
        help="Average daily consumption based on outgoing moves in the lookback period",
    )

    stock_status_color = fields.Integer(
        'Status Color',
        compute='_compute_restock_metrics',
        store=True,
        help="Color index for kanban cards: 1=red, 2=orange, 3=yellow, 10=green",
    )

    @api.depends('qty_available')
    def _compute_restock_metrics(self):
        """
        Calculate days of stock based on historical outgoing moves.
        """
        # Get configuration
        config = self.env['restock.kanban.config'].sudo().search([], limit=1)
        if not config:
            config = self.env['restock.kanban.config'].sudo().create({'name': 'Default'})
        
        lookback_days = config.lookback_days or 90
        healthy_threshold = config.healthy_threshold or 30
        warning_threshold = config.warning_threshold or 14
        critical_threshold = config.critical_threshold or 7

        from_date = fields.Datetime.now() - timedelta(days=lookback_days)

        for product in self:
            # Get outgoing moves for this product
            moves = self.env['stock.move'].sudo().search([
                ('product_id', '=', product.id),
                ('state', '=', 'done'),
                ('date', '>=', from_date),
                ('location_dest_id.usage', '=', 'customer'),
            ])
            
            total_consumed = sum(moves.mapped('quantity'))
            avg_daily = total_consumed / lookback_days if lookback_days > 0 else 0.0
            product.avg_daily_consumption = avg_daily

            # Calculate days of stock
            if avg_daily > 0:
                product.days_of_stock = product.qty_available / avg_daily
            else:
                if product.qty_available > 0:
                    product.days_of_stock = 999.0
                else:
                    product.days_of_stock = 0.0

            # Determine status based on thresholds
            days = product.days_of_stock
            qty = product.qty_available

            if qty <= 0 or days <= 0:
                product.stock_status = 'out_of_stock'
                product.stock_status_sequence = 1
                product.stock_status_color = 1
            elif days < critical_threshold:
                product.stock_status = 'critical'
                product.stock_status_sequence = 2
                product.stock_status_color = 2
            elif days < warning_threshold:
                product.stock_status = 'warning'
                product.stock_status_sequence = 3
                product.stock_status_color = 3
            else:
                product.stock_status = 'healthy'
                product.stock_status_sequence = 4
                product.stock_status_color = 10

    def action_reorder(self):
        """Open replenishment wizard for this product."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Replenish %s', self.display_name),
            'res_model': 'product.replenish',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_product_id': self.id,
                'default_product_tmpl_id': self.product_tmpl_id.id,
            },
        }
