from django.contrib import admin
from .models import Recipe, MealPlan, MealPlanItem, ShoppingList, ShoppingListItem, FavoriteRecipe, DietaryPreference, RecipeReview

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'dietary_type', 'is_shared', 'created_at')
    list_filter = ('dietary_type', 'is_shared', 'created_at')
    search_fields = ('title', 'user__username')

@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'recipe__title')


@admin.register(DietaryPreference)
class DietaryPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'vegan', 'vegetarian', 'gluten_free', 'updated_at')
    list_filter = ('vegan', 'vegetarian', 'gluten_free')
    search_fields = ('user__username',)


@admin.register(RecipeReview)
class RecipeReviewAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'reviewer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('recipe__title', 'reviewer__username')


@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username')

@admin.register(MealPlanItem)
class MealPlanItemAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'meal_date', 'meal_type', 'meal_plan')
    list_filter = ('meal_type', 'meal_date')

@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username')

@admin.register(ShoppingListItem)
class ShoppingListItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'quantity', 'is_checked', 'shopping_list')
    list_filter = ('is_checked',)
