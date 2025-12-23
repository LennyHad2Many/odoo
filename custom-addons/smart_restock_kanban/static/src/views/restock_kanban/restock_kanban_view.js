/** @odoo-module **/

import { kanbanView } from "@web/views/kanban/kanban_view";
import { registry } from "@web/core/registry";

export const restockKanbanView = {
    ...kanbanView,
    buttonTemplate: "smart_restock_kanban.RestockKanbanButtons",
};

registry.category("views").add("restock_kanban", restockKanbanView);
