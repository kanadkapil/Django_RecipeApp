import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipeapp.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from django.core.management import call_command

# Create migrations
print("Creating migrations for new models...")
call_command('makemigrations', 'recipes')
print("Applying migrations...")
call_command('migrate')
print("Done!")
