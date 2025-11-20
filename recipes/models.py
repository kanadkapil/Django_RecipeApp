from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Recipe(models.Model):
    DIETARY_CHOICES = [
        ('none', 'None'),
        ('vegan', 'Vegan'),
        ('vegetarian', 'Vegetarian'),
        ('gluten_free', 'Gluten-Free'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()  # Stored as comma-separated or newline-separated
    instructions = models.TextField()
    calories = models.IntegerField(validators=[MinValueValidator(0)])
    protein = models.FloatField(validators=[MinValueValidator(0)])  # in grams
    fat = models.FloatField(validators=[MinValueValidator(0)])  # in grams
    carbs = models.FloatField(validators=[MinValueValidator(0)])  # in grams
    dietary_type = models.CharField(max_length=20, choices=DIETARY_CHOICES, default='none')
    is_shared = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'recipe']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} favorited {self.recipe.title}"


class DietaryPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dietary_preference')
    vegan = models.BooleanField(default=False)
    vegetarian = models.BooleanField(default=False)
    gluten_free = models.BooleanField(default=False)
    nut_allergy = models.BooleanField(default=False)
    dairy_free = models.BooleanField(default=False)
    low_carb = models.BooleanField(default=False)
    custom_restrictions = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dietary preferences for {self.user.username}"


class RecipeReview(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['recipe', 'reviewer']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review of {self.recipe.title} by {self.reviewer.username}"


class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_plans')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"


class MealPlanItem(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='items')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    meal_date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    
    class Meta:
        unique_together = ['meal_plan', 'meal_date', 'meal_type']
    
    def __str__(self):
        return f"{self.recipe.title} - {self.meal_date} ({self.meal_type})"


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shopping_lists')
    name = models.CharField(max_length=255)
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='shopping_lists')  # Link to meal plan
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"


class ShoppingListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=100)
    is_checked = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.item_name} ({self.quantity})"
