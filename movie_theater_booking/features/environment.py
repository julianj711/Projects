import django
from django.test.utils import setup_test_environment
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'movie_theater_booking.settings'
django.setup()

def before_scenario(context, scenario):
    from django.test.runner import DiscoverRunner
    context.runner = DiscoverRunner(verbosity=0)
    context.old_config = context.runner.setup_databases()

def after_scenario(context, scenario):
    context.runner.teardown_databases(context.old_config)