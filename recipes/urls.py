from django.urls import path
from . import views, api_views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('nutrition-summary/', views.nutritional_summary, name='nutritional_summary'),
    
    # Recipes
    path('recipes/', views.my_recipes, name='my_recipes'),
    path('recipes/add/', views.add_recipe, name='add_recipe'),
    path('recipes/<int:pk>/', views.view_recipe, name='view_recipe'),
    path('recipes/<int:pk>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipes/<int:pk>/delete/', views.delete_recipe, name='delete_recipe'),
    path('recipes/<int:pk>/share/', views.share_recipe, name='share_recipe'),  # Added share recipe URL
    path('shared-recipes/', views.shared_recipes, name='shared_recipes'),
    
    path('recipes/<int:recipe_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_recipes, name='favorite_recipes'),
    path('recipes/<int:recipe_id>/review/', views.add_review, name='add_review'),
    
    path('dietary-preferences/', views.manage_dietary_preferences, name='manage_dietary_preferences'),
    
    # Meal Plans
    path('meal-plans/', views.meal_plans, name='meal_plans'),
    path('meal-plans/create/', views.create_meal_plan, name='create_meal_plan'),
    path('meal-plans/<int:pk>/', views.view_meal_plan, name='view_meal_plan'),
    path('meal-plans/<int:meal_plan_id>/add-item/', views.add_meal_plan_item, name='add_meal_plan_item'),
    path('meal-plan-items/<int:item_id>/delete/', views.delete_meal_plan_item, name='delete_meal_plan_item'),
    
    path('meal-plans/<int:meal_plan_id>/generate-shopping-list/', views.generate_shopping_list_from_meal_plan, name='generate_shopping_list'),
    
    # Shopping Lists
    path('shopping-lists/', views.shopping_lists, name='shopping_lists'),
    path('shopping-lists/create/', views.create_shopping_list, name='create_shopping_list'),
    path('shopping-lists/<int:pk>/', views.view_shopping_list, name='view_shopping_list'),
    path('shopping-lists/<int:shopping_list_id>/add-item/', views.add_shopping_item, name='add_shopping_item'),
    path('shopping-list-items/<int:item_id>/delete/', views.delete_shopping_item, name='delete_shopping_item'),
    path('shopping-list-items/<int:item_id>/toggle/', views.toggle_shopping_item, name='toggle_shopping_item'),
    
    path('api/favorites/', api_views.api_favorite_recipes, name='api_favorites'),
    path('api/recipes/<int:recipe_id>/', api_views.api_recipe_details, name='api_recipe_details'),
    path('api/stats/', api_views.api_user_stats, name='api_user_stats'),
    path('api/search/', api_views.api_search_recipes, name='api_search_recipes'),
    path('api/recipes/<int:recipe_id>/favorite/', api_views.api_toggle_favorite, name='api_toggle_favorite'),
    path('api/recipes/<int:recipe_id>/review/', api_views.api_add_review, name='api_add_review'),
    path('api/meal-plans/<int:meal_plan_id>/nutrition/', api_views.api_meal_plan_nutrition, name='api_meal_plan_nutrition'),
]
