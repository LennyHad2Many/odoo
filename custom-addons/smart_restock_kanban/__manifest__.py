{
    'name': 'Smart Restock Kanban',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Visual inventory dashboard with smart stock status tracking',
    'description': """
Smart Restock Kanban Board
==========================

A visual kanban board that automatically categorizes products based on
projected days of stock remaining:

* **Out of Stock** (Red): 0 or negative days
* **Critical** (Orange): < 7 days
* **Warning** (Yellow): 7-14 days
* **Healthy** (Green): > 30 days

Features:
- Automatic categorization based on sales consumption
- One-click reorder action
- Warehouse filtering
- Product category filtering
- Configurable thresholds
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': ['stock', 'product'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/restock_config_data.xml',
        'views/restock_config_views.xml',
        'views/product_restock_kanban_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'smart_restock_kanban/static/src/views/restock_kanban/*.js',
            'smart_restock_kanban/static/src/xml/*.xml',
            'smart_restock_kanban/static/src/scss/*.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
