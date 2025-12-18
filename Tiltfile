# Odoo Development Environment
# Run with: tilt up

# Use docker-compose for local development
docker_compose('./docker-compose.yml')

# Resource configuration
dc_resource('odoo', labels=['app'])
dc_resource('postgres', labels=['database'])

# Port forwards (already defined in docker-compose, but explicit here)
# Odoo web interface: http://localhost:8069

# Watch for changes in custom addons and trigger reload
watch_file('./custom-addons')
watch_file('./config')

# Local resource for logs
local_resource(
    'odoo-logs',
    serve_cmd='docker compose logs -f odoo',
    labels=['logs']
)

# Convenience commands
local_resource(
    'odoo-shell',
    cmd='echo "Run: docker compose exec odoo odoo shell -d <dbname>"',
    labels=['tools'],
    auto_init=False,
    trigger_mode=TRIGGER_MODE_MANUAL
)

local_resource(
    'db-reset',
    cmd='docker compose down -v && docker compose up -d',
    labels=['tools'],
    auto_init=False,
    trigger_mode=TRIGGER_MODE_MANUAL
)
