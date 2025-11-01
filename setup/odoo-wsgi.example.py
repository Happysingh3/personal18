import odoo

# Server wide modules (default)
odoo.conf.server_wide_modules = ['base', 'web']

# Config object
conf = odoo.tools.config

# Addons path mein default addons ke sath aapke custom addons ka path bhi add karen
conf['addons_path'] = (
    r'C:\Users\Admin\OneDrive - Aebocode Technologies\Desktop\Odoo_18\Odoo_18\odoo\addons,'
    r'C:\Users\Admin\OneDrive - Aebocode Technologies\Desktop\Odoo_18\Odoo_18\odoo\custom_addons'
)

# Local database connection settings
conf['db_host'] = 'localhost'     # Agar DB local hai toh 'localhost'
conf['db_port'] = 5432            # PostgreSQL default port
conf['db_user'] = 'odoo'          # Aapka DB user, apne hisaab se badal sakte hain
conf['db_password'] = 'odoo' # DB password, apne hisaab se badal sakte hain
conf['db_name'] = False           # False means koi fixed DB nahi, sab access hoga

# WSGI application
application = odoo.http.root

# Load server wide modules (base, web, etc.)
odoo.service.server.load_server_wide_modules()

# Gunicorn settings (optional, agar Gunicorn use kar rahe hain)
bind = '127.0.0.1:8069'
pidfile = '.gunicorn.pid'
workers = 4
timeout = 240
max_requests = 2000
