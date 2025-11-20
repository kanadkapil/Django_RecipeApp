from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Recipe, MealPlan, ShoppingList, ShoppingListItem, RecipeReview, DietaryPreference

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 
                  'calories', 'protein', 'fat', 'carbs', 'dietary_type', 'is_shared']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Recipe title'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Recipe description'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5, 'placeholder': 'List ingredients (one per line)'}),
            'instructions': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 6, 'placeholder': 'Step-by-step instructions'}),
            'calories': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Calories'}),
            'protein': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Protein (g)', 'step': '0.1'}),
            'fat': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Fat (g)', 'step': '0.1'}),
            'carbs': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Carbs (g)', 'step': '0.1'}),
            'dietary_type': forms.Select(attrs={'class': 'form-select'}),
            'is_shared': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Meal plan name'}),
        }


class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Shopping list name'}),
        }


class ShoppingListItemForm(forms.ModelForm):
    class Meta:
        model = ShoppingListItem
        fields = ['item_name', 'quantity']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Item name'}),
            'quantity': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Quantity (e.g., 2 cups)'}),
        }


class RecipeReviewForm(forms.ModelForm):
    class Meta:
        model = RecipeReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-input', 'type': 'range', 'min': '1', 'max': '5'}),
            'comment': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Share your thoughts...'}),
        }


class DietaryPreferenceForm(forms.ModelForm):
    class Meta:
        model = DietaryPreference
        fields = ['vegan', 'vegetarian', 'gluten_free', 'nut_allergy', 'dairy_free', 'low_carb', 'custom_restrictions']
        widgets = {
            'vegan': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'vegetarian': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'gluten_free': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'nut_allergy': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'dairy_free': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'low_carb': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'custom_restrictions': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Any custom dietary restrictions...'}),
        }
