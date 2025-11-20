# RecipeApp - Django Recipe Management Application

A full-featured Django application for managing recipes, meal plans, and shopping lists with user authentication.

## Features

- **User Authentication**: Register, login, logout
- **Recipe Management**: Create, read, update, delete recipes with nutrition info
- **Dietary Filtering**: Filter recipes by dietary type (vegan, vegetarian, gluten-free)
- **Recipe Sharing**: Mark recipes as shareable and browse shared recipes
- **Meal Planning**: Create meal plans and assign recipes to specific dates and meal types
- **Shopping Lists**: Create shopping lists and manage items with checkoff functionality
- **User Privacy**: Each user sees only their own recipes, meal plans, and shopping lists

## Installation & Setup

1. **Create a virtual environment** (recommended):
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

2. **Install dependencies**:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Run migrations** to create the database:
   \`\`\`bash
   python manage.py migrate
   \`\`\`

4. **Create a superuser** (admin account):
   \`\`\`bash
   python manage.py createsuperuser
   \`\`\`

5. **Run the development server**:
   \`\`\`bash
   python manage.py runserver
   \`\`\`

6. **Access the application**:
   - Main site: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/

## Project Structure

\`\`\`
recipeapp/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── db.sqlite3               # SQLite database
├── recipeapp/
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── __init__.py
├── recipes/
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── forms.py             # Django forms
│   ├── urls.py              # Recipe app URLs
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App configuration
│   └── __init__.py
├── templates/
│   ├── base.html            # Base template
│   └── recipes/
│       ├── home.html
│       ├── login.html
│       ├── register.html
│       ├── my_recipes.html
│       ├── add_recipe.html
│       ├── edit_recipe.html
│       ├── view_recipe.html
│       ├── shared_recipes.html
│       ├── meal_plans.html
│       ├── create_meal_plan.html
│       ├── view_meal_plan.html
│       ├── add_meal_plan_item.html
│       ├── shopping_lists.html
│       ├── create_shopping_list.html
│       ├── view_shopping_list.html
│       └── add_shopping_item.html
└── static/
    └── style.css            # Styling

\`\`\`

## Usage

### Creating an Account
1. Click "Register" on the home page
2. Enter username, email, and password
3. Login with your credentials

### Adding Recipes
1. Click "Add Recipe" in the navigation
2. Fill in recipe details including title, ingredients, instructions, and nutrition info
3. Select dietary type
4. Toggle "Shared" if you want other users to see it
5. Save the recipe

### Creating Meal Plans
1. Navigate to "Meal Plans"
2. Click "Create New Plan"
3. Enter a name (e.g., "Week of Dec 4-10")
4. Click "Add Recipe" to assign recipes to specific dates and meal times
5. View your organized meal plan

### Managing Shopping Lists
1. Go to "Shopping Lists"
2. Create a new list
3. Add items with quantities
4. Check off items as you shop
5. Delete items when done

### Sharing Recipes
1. When creating/editing a recipe, check the "Shared" box
2. Your recipe appears on the "Browse Recipes" page for other users
3. Other users can view your shared recipes

## Database Models

### Recipe
- Title, Description, Ingredients, Instructions
- Nutrition info (calories, protein, fat, carbs)
- Dietary type (vegan, vegetarian, gluten-free, none)
- Is shared flag
- User foreign key

### MealPlan
- Name, User foreign key
- Timestamps

### MealPlanItem
- Recipe foreign key, Meal plan foreign key
- Meal date, Meal type (breakfast/lunch/dinner/snack)

### ShoppingList
- Name, User foreign key
- Timestamps

### ShoppingListItem
- Item name, Quantity
- Is checked flag
- Shopping list foreign key

## Technologies Used

- **Backend**: Django 4.2
- **Database**: SQLite
- **Frontend**: HTML5, CSS3
- **Authentication**: Django built-in auth

## Future Enhancements

- Recipe images
- Ingredient quantity multipliers for meal plans
- Export meal plans and shopping lists to PDF
- Recipe ratings and reviews
- Search functionality
- Mobile app

## License

This project is open source and available under the MIT License.
