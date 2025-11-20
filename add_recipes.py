import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipeapp.settings')
django.setup()

from recipes.models import Recipe
from django.contrib.auth.models import User

user = User.objects.get(username="kanad")

recipes = [
    # same list from above...
]

for r in recipes:
    Recipe.objects.create(user=user, **r)

print("✓ Added 5 recipes!")
