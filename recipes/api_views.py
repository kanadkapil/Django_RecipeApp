from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from .models import Recipe, FavoriteRecipe, MealPlan, ShoppingList, RecipeReview
import json

@login_required
@require_http_methods(["GET"])
def api_favorite_recipes(request):
    """Get user's favorite recipes"""
    favorites = FavoriteRecipe.objects.filter(user=request.user).select_related('recipe')
    recipes = [
        {
            'id': fav.recipe.id,
            'title': fav.recipe.title,
            'description': fav.recipe.description,
            'calories': fav.recipe.calories,
            'protein': fav.recipe.protein,
            'fat': fav.recipe.fat,
            'carbs': fav.recipe.carbs,
            'dietary_type': fav.recipe.dietary_type,
            'created_at': fav.recipe.created_at.isoformat(),
        }
        for fav in favorites
    ]
    return JsonResponse({'favorites': recipes})


@login_required
@require_http_methods(["GET"])
def api_recipe_details(request, recipe_id):
    """Get detailed recipe information with reviews"""
    recipe = Recipe.objects.get(pk=recipe_id)
    if not recipe.is_shared and recipe.user != request.user:
        return JsonResponse({'error': 'Not found'}, status=404)
    
    reviews = RecipeReview.objects.filter(recipe=recipe).select_related('reviewer')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    is_favorite = FavoriteRecipe.objects.filter(user=request.user, recipe=recipe).exists()
    
    data = {
        'id': recipe.id,
        'title': recipe.title,
        'description': recipe.description,
        'ingredients': recipe.ingredients.split('\n'),
        'instructions': recipe.instructions,
        'calories': recipe.calories,
        'protein': recipe.protein,
        'fat': recipe.fat,
        'carbs': recipe.carbs,
        'dietary_type': recipe.dietary_type,
        'is_shared': recipe.is_shared,
        'is_favorite': is_favorite,
        'avg_rating': avg_rating,
        'review_count': reviews.count(),
        'reviews': [
            {
                'reviewer': review.reviewer.username,
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at.isoformat(),
            }
            for review in reviews
        ],
    }
    return JsonResponse(data)


@login_required
@require_http_methods(["GET"])
def api_user_stats(request):
    """Get user statistics"""
    total_recipes = Recipe.objects.filter(user=request.user).count()
    favorite_count = FavoriteRecipe.objects.filter(user=request.user).count()
    total_meal_plans = MealPlan.objects.filter(user=request.user).count()
    total_shopping_lists = ShoppingList.objects.filter(user=request.user).count()
    
    data = {
        'total_recipes': total_recipes,
        'favorite_count': favorite_count,
        'total_meal_plans': total_meal_plans,
        'total_shopping_lists': total_shopping_lists,
    }
    return JsonResponse(data)


@login_required
@require_http_methods(["GET"])
def api_search_recipes(request):
    """Search shared recipes"""
    query = request.GET.get('q', '')
    dietary_filter = request.GET.get('dietary_type', '')
    
    recipes = Recipe.objects.filter(is_shared=True)
    
    if query:
        from django.db.models import Q
        recipes = recipes.filter(Q(title__icontains=query) | Q(description__icontains=query))
    
    if dietary_filter:
        recipes = recipes.filter(dietary_type=dietary_filter)
    
    recipes = recipes.annotate(avg_rating=Avg('reviews__rating')).values(
        'id', 'title', 'description', 'calories', 'dietary_type', 'avg_rating'
    )[:20]
    
    return JsonResponse({'results': list(recipes)})


@login_required
@require_http_methods(["POST"])
def api_toggle_favorite(request, recipe_id):
    """Toggle recipe favorite status"""
    recipe = Recipe.objects.get(pk=recipe_id)
    if not recipe.is_shared and recipe.user != request.user:
        return JsonResponse({'error': 'Not found'}, status=404)
    
    favorite, created = FavoriteRecipe.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True
    
    return JsonResponse({'is_favorite': is_favorite})


@login_required
@require_http_methods(["POST"])
def api_add_review(request, recipe_id):
    """Add or update recipe review"""
    recipe = Recipe.objects.get(pk=recipe_id)
    if not recipe.is_shared and recipe.user != request.user:
        return JsonResponse({'error': 'Not found'}, status=404)
    
    try:
        data = json.loads(request.body)
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        review, created = RecipeReview.objects.update_or_create(
            recipe=recipe,
            reviewer=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        
        avg_rating = recipe.reviews.aggregate(Avg('rating'))['rating__avg']
        
        return JsonResponse({
            'success': True,
            'avg_rating': avg_rating,
            'review_count': recipe.reviews.count(),
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_http_methods(["GET"])
def api_meal_plan_nutrition(request, meal_plan_id):
    """Get meal plan nutritional summary"""
    from .models import MealPlanItem
    
    meal_plan = MealPlan.objects.get(pk=meal_plan_id, user=request.user)
    items = MealPlanItem.objects.filter(meal_plan=meal_plan)
    
    total_calories = sum(item.recipe.calories for item in items)
    total_protein = sum(item.recipe.protein for item in items)
    total_fat = sum(item.recipe.fat for item in items)
    total_carbs = sum(item.recipe.carbs for item in items)
    
    return JsonResponse({
        'meal_plan_id': meal_plan.id,
        'name': meal_plan.name,
        'total_calories': total_calories,
        'total_protein': total_protein,
        'total_fat': total_fat,
        'total_carbs': total_carbs,
        'item_count': items.count(),
    })
