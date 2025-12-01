import os
import sys

# ============================================
# Django WSGI Configuration for cPanel
# ============================================

# IMPORTANT: Update these paths for your cPanel setup
CPANEL_USERNAME = 'your_cpanel_username'  # Change this!
PROJECT_NAME = 'vhorla'  # Your project folder name

# Add your project directory to the sys.path
project_home = f'/home/{CPANEL_USERNAME}/public_html/{PROJECT_NAME}'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable to tell Django where settings are
os.environ['DJANGO_SETTINGS_MODULE'] = 'marketplace.settings'

# Activate virtual environment
venv_path = os.path.join(project_home, 'venv/bin/activate_this.py')
if os.path.exists(venv_path):
    with open(venv_path) as f:
        exec(f.read(), {'__file__': venv_path})

# Import and configure Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
