from self_quantify_app import app_factory
import os


environment = os.environ.get('DEPLOYMENT', 'local')
app = app_factory(environment)
