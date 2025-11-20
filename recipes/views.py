from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Avg, Count
from .models import Recipe, MealPlan, MealPlanItem, ShoppingList, ShoppingListItem, FavoriteRecipe, DietaryPreference, RecipeReview
from .forms import RegisterForm, LoginForm, RecipeForm, MealPlanForm, ShoppingListForm, ShoppingListItemForm
from datetime import datetime
import urllib.parse

def home(request):
    shared_recipes = Recipe.objects.filter(is_shared=True).order_by('-created_at')[:6]
    context = {
        'shared_recipes': shared_recipes,
    }
    return render(request, 'recipes/home.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'recipes/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'recipes/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(user=request.user)
    dietary_filter = request.GET.get('dietary_type')
    
    if dietary_filter:
        recipes = recipes.filter(dietary_type=dietary_filter)
    
    context = {
        'recipes': recipes,
        'dietary_choices': Recipe.DIETARY_CHOICES,
        'current_filter': dietary_filter,
    }
    return render(request, 'recipes/my_recipes.html', context)


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            return redirect('my_recipes')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})


@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('my_recipes')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/edit_recipe.html', {'form': form, 'recipe': recipe})


@login_required
@require_http_methods(["POST"])
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    recipe.delete()
    return redirect('my_recipes')


@login_required
def favorite_recipes(request):
    favorites = FavoriteRecipe.objects.filter(user=request.user).select_related('recipe')
    recipes = [fav.recipe for fav in favorites]
    dietary_filter = request.GET.get('dietary_type')
    
    if dietary_filter:
        recipes = [r for r in recipes if r.dietary_type == dietary_filter]
    
    context = {
        'recipes': recipes,
        'dietary_choices': Recipe.DIETARY_CHOICES,
        'current_filter': dietary_filter,
        'is_favorites': True,
    }
    return render(request, 'recipes/my_recipes.html', context)


@login_required
@require_http_methods(["POST"])
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if not recipe.is_shared and recipe.user != request.user:
        return redirect('home')
    
    favorite, created = FavoriteRecipe.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        favorite.delete()
    
    return redirect('view_recipe', pk=recipe_id)


def shared_recipes(request):
    recipes = Recipe.objects.filter(is_shared=True)
    recipes = recipes.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    )
    dietary_filter = request.GET.get('dietary_type')
    search_query = request.GET.get('search', '')
    
    if dietary_filter:
        recipes = recipes.filter(dietary_type=dietary_filter)
    
    if search_query:
        recipes = recipes.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    
    context = {
        'recipes': recipes,
        'dietary_choices': Recipe.DIETARY_CHOICES,
        'current_filter': dietary_filter,
        'search_query': search_query,
    }
    return render(request, 'recipes/shared_recipes.html', context)


def view_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if not recipe.is_shared and recipe.user != request.user:
        return redirect('home')
    
    reviews = RecipeReview.objects.filter(recipe=recipe).select_related('reviewer')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    is_favorite = False
    
    if request.user.is_authenticated:
        is_favorite = FavoriteRecipe.objects.filter(user=request.user, recipe=recipe).exists()
    
    context = {
        'recipe': recipe,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'is_favorite': is_favorite,
    }
    return render(request, 'recipes/view_recipe.html', context)


@login_required
def add_review(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if not recipe.is_shared and recipe.user != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        
        review, created = RecipeReview.objects.update_or_create(
            recipe=recipe,
            reviewer=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        return redirect('view_recipe', pk=recipe_id)
    
    existing_review = RecipeReview.objects.filter(recipe=recipe, reviewer=request.user).first()
    context = {
        'recipe': recipe,
        'existing_review': existing_review,
    }
    return render(request, 'recipes/add_review.html', context)


@login_required
def manage_dietary_preferences(request):
    dietary_pref, created = DietaryPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        dietary_pref.vegan = request.POST.get('vegan') == 'on'
        dietary_pref.vegetarian = request.POST.get('vegetarian') == 'on'
        dietary_pref.gluten_free = request.POST.get('gluten_free') == 'on'
        dietary_pref.nut_allergy = request.POST.get('nut_allergy') == 'on'
        dietary_pref.dairy_free = request.POST.get('dairy_free') == 'on'
        dietary_pref.low_carb = request.POST.get('low_carb') == 'on'
        dietary_pref.custom_restrictions = request.POST.get('custom_restrictions', '')
        dietary_pref.save()
        return redirect('my_recipes')
    
    context = {'dietary_preference': dietary_pref}
    return render(request, 'recipes/manage_dietary_preferences.html', context)


@login_required
def generate_shopping_list_from_meal_plan(request, meal_plan_id):
    meal_plan = get_object_or_404(MealPlan, pk=meal_plan_id, user=request.user)
    
    meal_items = MealPlanItem.objects.filter(meal_plan=meal_plan)
    
    shopping_list = ShoppingList.objects.create(
        user=request.user,
        name=f"Shopping List for {meal_plan.name}",
        meal_plan=meal_plan
    )
    
    ingredient_set = set()
    for item in meal_items:
        ingredients = item.recipe.ingredients.split('\n')
        for ingredient in ingredients:
            ingredient = ingredient.strip()
            if ingredient:
                ingredient_set.add(ingredient)
    
    for ingredient in sorted(ingredient_set):
        ShoppingListItem.objects.create(
            shopping_list=shopping_list,
            item_name=ingredient,
            quantity='1'
        )
    
    return redirect('view_shopping_list', pk=shopping_list.id)


@login_required
def meal_plans(request):
    meal_plans = MealPlan.objects.filter(user=request.user)
    context = {'meal_plans': meal_plans}
    return render(request, 'recipes/meal_plans.html', context)


@login_required
def create_meal_plan(request):
    if request.method == 'POST':
        form = MealPlanForm(request.POST)
        if form.is_valid():
            meal_plan = form.save(commit=False)
            meal_plan.user = request.user
            meal_plan.save()
            return redirect('meal_plans')
    else:
        form = MealPlanForm()
    return render(request, 'recipes/create_meal_plan.html', {'form': form})


@login_required
def view_meal_plan(request, pk):
    meal_plan = get_object_or_404(MealPlan, pk=pk, user=request.user)
    items = MealPlanItem.objects.filter(meal_plan=meal_plan).order_by('meal_date', 'meal_type')
    
    total_calories = sum(item.recipe.calories for item in items)
    total_protein = sum(item.recipe.protein for item in items)
    total_fat = sum(item.recipe.fat for item in items)
    total_carbs = sum(item.recipe.carbs for item in items)
    
    context = {
        'meal_plan': meal_plan,
        'items': items,
        'meal_type_choices': MealPlanItem.MEAL_TYPES,
        'total_calories': total_calories,
        'total_protein': total_protein,
        'total_fat': total_fat,
        'total_carbs': total_carbs,
    }
    return render(request, 'recipes/view_meal_plan.html', context)


@login_required
def add_meal_plan_item(request, meal_plan_id):
    meal_plan = get_object_or_404(MealPlan, pk=meal_plan_id, user=request.user)
    recipes = Recipe.objects.filter(user=request.user)
    
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        meal_date = request.POST.get('meal_date')
        meal_type = request.POST.get('meal_type')
        
        recipe = get_object_or_404(Recipe, pk=recipe_id, user=request.user)
        item = MealPlanItem(meal_plan=meal_plan, recipe=recipe, meal_date=meal_date, meal_type=meal_type)
        item.save()
        return redirect('view_meal_plan', pk=meal_plan_id)
    
    context = {
        'meal_plan': meal_plan,
        'recipes': recipes,
        'meal_type_choices': MealPlanItem.MEAL_TYPES,
    }
    return render(request, 'recipes/add_meal_plan_item.html', context)


@login_required
@require_http_methods(["POST"])
def delete_meal_plan_item(request, item_id):
    item = get_object_or_404(MealPlanItem, pk=item_id)
    meal_plan_id = item.meal_plan.id
    item.delete()
    return redirect('view_meal_plan', pk=meal_plan_id)


@login_required
def shopping_lists(request):
    shopping_lists = ShoppingList.objects.filter(user=request.user)
    context = {'shopping_lists': shopping_lists}
    return render(request, 'recipes/shopping_lists.html', context)


@login_required
def create_shopping_list(request):
    if request.method == 'POST':
        form = ShoppingListForm(request.POST)
        if form.is_valid():
            shopping_list = form.save(commit=False)
            shopping_list.user = request.user
            shopping_list.save()
            return redirect('shopping_lists')
    else:
        form = ShoppingListForm()
    return render(request, 'recipes/create_shopping_list.html', {'form': form})


@login_required
def view_shopping_list(request, pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk, user=request.user)
    items = ShoppingListItem.objects.filter(shopping_list=shopping_list)
    context = {
        'shopping_list': shopping_list,
        'items': items,
    }
    return render(request, 'recipes/view_shopping_list.html', context)


@login_required
def add_shopping_item(request, shopping_list_id):
    shopping_list = get_object_or_404(ShoppingList, pk=shopping_list_id, user=request.user)
    
    if request.method == 'POST':
        form = ShoppingListItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.shopping_list = shopping_list
            item.save()
            return redirect('view_shopping_list', pk=shopping_list_id)
    else:
        form = ShoppingListItemForm()
    
    context = {
        'shopping_list': shopping_list,
        'form': form,
    }
    return render(request, 'recipes/add_shopping_item.html', context)


@login_required
@require_http_methods(["POST"])
def delete_shopping_item(request, item_id):
    item = get_object_or_404(ShoppingListItem, pk=item_id)
    shopping_list_id = item.shopping_list.id
    item.delete()
    return redirect('view_shopping_list', pk=shopping_list_id)


@login_required
@require_http_methods(["POST"])
def toggle_shopping_item(request, item_id):
    item = get_object_or_404(ShoppingListItem, pk=item_id)
    item.is_checked = not item.is_checked
    item.save()
    return redirect('view_shopping_list', pk=item.shopping_list.id)


@login_required
def dashboard(request):
    # Get user's recipes
    total_recipes = Recipe.objects.filter(user=request.user).count()
    
    # Get favorite recipes
    favorite_count = FavoriteRecipe.objects.filter(user=request.user).count()
    
    # Get meal plan stats
    recent_meal_plans = MealPlan.objects.filter(user=request.user).order_by('-created_at')[:5]
    total_meal_plans = recent_meal_plans.count()
    
    # Get shopping list stats
    recent_shopping_lists = ShoppingList.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Calculate nutrition stats from recent meal plans
    nutrition_stats = {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0}
    for meal_plan in recent_meal_plans[:1]:  # Latest meal plan
        items = MealPlanItem.objects.filter(meal_plan=meal_plan)
        nutrition_stats['calories'] = sum(item.recipe.calories for item in items)
        nutrition_stats['protein'] = sum(item.recipe.protein for item in items)
        nutrition_stats['fat'] = sum(item.recipe.fat for item in items)
        nutrition_stats['carbs'] = sum(item.recipe.carbs for item in items)
    
    # Get user's dietary preferences
    dietary_pref = DietaryPreference.objects.filter(user=request.user).first()
    
    context = {
        'total_recipes': total_recipes,
        'favorite_count': favorite_count,
        'total_meal_plans': total_meal_plans,
        'recent_meal_plans': recent_meal_plans,
        'recent_shopping_lists': recent_shopping_lists,
        'nutrition_stats': nutrition_stats,
        'dietary_preference': dietary_pref,
    }
    return render(request, 'recipes/dashboard.html', context)


@login_required
def nutritional_summary(request):
    # Get all recipes with their nutritional information
    recipes = Recipe.objects.filter(user=request.user)
    
    total_recipes = recipes.count()
    avg_calories = sum(r.calories for r in recipes) / total_recipes if total_recipes > 0 else 0
    avg_protein = sum(r.protein for r in recipes) / total_recipes if total_recipes > 0 else 0
    avg_fat = sum(r.fat for r in recipes) / total_recipes if total_recipes > 0 else 0
    avg_carbs = sum(r.carbs for r in recipes) / total_recipes if total_recipes > 0 else 0
    
    # Dietary breakdown
    dietary_stats = {}
    for diet_type, diet_label in Recipe.DIETARY_CHOICES:
        count = recipes.filter(dietary_type=diet_type).count()
        dietary_stats[diet_label] = count
    
    context = {
        'total_recipes': total_recipes,
        'avg_calories': round(avg_calories, 1),
        'avg_protein': round(avg_protein, 1),
        'avg_fat': round(avg_fat, 1),
        'avg_carbs': round(avg_carbs, 1),
        'dietary_stats': dietary_stats,
    }
    return render(request, 'recipes/nutritional_summary.html', context)


@login_required
def share_recipe(request, pk):
    """Handle recipe sharing via email or social media"""
    recipe = get_object_or_404(Recipe, pk=pk)
    if not recipe.is_shared and recipe.user != request.user:
        return redirect('home')
    
    share_url = request.build_absolute_uri(f'/recipes/{recipe.id}/')
    share_text = f"Check out this amazing {recipe.title} recipe!"
    
    context = {
        'recipe': recipe,
        'share_url': share_url,
        'share_text': share_text,
        'encoded_url': urllib.parse.quote(share_url),
        'encoded_text': urllib.parse.quote(share_text),
    }
    return render(request, 'recipes/share_recipe.html', context)
