# RecipeApp - Complete Feature Documentation

## Overview
RecipeApp is a comprehensive Django-based recipe and meal planning application with a modern frontend. This document outlines all features and how to use them.

## Core Features

### 1. User Authentication
- Register with username, email, and password
- Secure login/logout functionality
- User-specific data isolation

### 2. Recipe Management

#### Create & Edit Recipes
- Add detailed recipes with:
  - Title and description
  - Ingredient list (one per line)
  - Step-by-step instructions
  - Complete nutritional information (calories, protein, fat, carbs)
  - Dietary type classification
  - Option to share publicly

#### Recipe Discovery
- View shared recipes from other users
- Filter recipes by dietary type
- Search recipes by title or description
- View detailed recipe information including ingredients, instructions, and nutrition

#### Favorite Recipes
- Save favorite recipes for quick access
- Dedicated favorites view
- Toggle favorite status from recipe pages

### 3. Recipe Reviews & Ratings

#### Leave Reviews
- Rate recipes from 1-5 stars
- Write detailed comments about recipes
- Edit your existing reviews
- View average ratings and review count

#### View Reviews
- See ratings and comments from other users
- Check community feedback before trying recipes
- Track recipe popularity

### 4. Meal Planning

#### Create Meal Plans
- Create custom meal plans with any name
- Organize recipes by date and meal type (breakfast, lunch, dinner, snack)
- View nutritional summary for entire meal plan

#### Auto-Generate Shopping Lists
- One-click shopping list generation from meal plans
- Automatically extracts all ingredients
- Links shopping list to source meal plan

#### Nutrition Tracking
- View total nutritional information for meal plans
- Track aggregate calories, protein, fat, and carbs
- Optimize meals for dietary goals

### 5. Shopping Lists

#### Create & Manage Lists
- Create custom shopping lists
- Add items with quantities
- Check off items as you shop
- Mark items as complete/incomplete
- Delete items when done

#### Features
- Auto-generated from meal plans
- Manual item addition
- Quantity tracking
- Progress indicators

### 6. Dietary Preferences

#### Personal Dietary Restrictions
- Mark dietary preferences:
  - Vegan
  - Vegetarian
  - Gluten-Free
  - Nut Allergy
  - Dairy-Free
  - Low-Carb
  - Custom restrictions

#### Usage
- Profile appears on dashboard
- Use for dietary goal tracking
- Filter recipes by your restrictions

### 7. Nutritional Tracking

#### Dashboard
- Quick stats overview
- Recent recipes, meal plans, and shopping lists
- Current dietary preferences
- Nutrition overview from latest meal plan

#### Nutrition Summary
- Average nutrition per recipe
- Dietary type breakdown
- Visual statistics for meal planning

### 8. Recipe Sharing

#### Share Your Recipes
- Mark recipes as "shared" when creating/editing
- Public recipes appear on browse page
- Receive ratings and reviews from community

#### Shared Recipe Library
- Browse all shared recipes
- Search by keyword
- Filter by dietary type
- See community ratings

### 9. API Endpoints

For frontend integration (React/Next.js):

#### Recipes
- `GET /api/search/` - Search shared recipes
- `GET /api/recipes/<id>/` - Get recipe details
- `POST /api/recipes/<id>/favorite/` - Toggle favorite
- `POST /api/recipes/<id>/review/` - Add/update review

#### User Data
- `GET /api/stats/` - Get user statistics
- `GET /api/favorites/` - Get favorite recipes
- `GET /api/meal-plans/<id>/nutrition/` - Get meal plan nutrition

## Database Models

### Recipe
- Title, description, ingredients, instructions
- Nutritional info (calories, protein, fat, carbs)
- Dietary type
- Shared status
- User association
- Timestamps

### FavoriteRecipe
- User foreign key
- Recipe foreign key
- Unique constraint (user can't favorite same recipe twice)

### DietaryPreference
- User one-to-one relationship
- Multiple boolean fields for restrictions
- Custom restrictions text field

### RecipeReview
- Recipe and reviewer foreign keys
- 1-5 star rating
- Comment text
- Unique constraint (one review per user per recipe)
- Timestamps

### MealPlan & MealPlanItem
- Plan name and user association
- Items link recipes to dates and meal types
- Unique constraint on date + meal type per plan

### ShoppingList & ShoppingListItem
- List name and user association
- Optional meal plan linkage
- Items with name, quantity, and check status
- Timestamps

## Usage Examples

### Adding Your First Recipe
1. Click "Add Recipe" in navigation
2. Fill in title, description, and ingredients
3. Enter nutritional information
4. Select dietary type
5. Check "Shared" if you want to share publicly
6. Save the recipe

### Creating a Weekly Meal Plan
1. Go to "Meal Plans"
2. Click "Create New Plan"
3. Name it (e.g., "Week of Jan 1-7")
4. Add recipes for each day and meal type
5. View nutritional totals
6. Generate shopping list

### Auto-Generating Shopping List
1. View a meal plan
2. Click "Generate Shopping List"
3. App extracts all ingredients
4. Review and modify as needed
5. Check off items while shopping

### Finding Recipes for Your Diet
1. Go to "Browse Recipes"
2. Use search or filter by dietary type
3. Check ratings and reviews
4. Click recipe to view details
5. Add to favorites or save for later

## Future Enhancements

- Recipe images and gallery
- Export to PDF functionality
- Mobile application
- Recipe ratings distribution
- Ingredient substitutions
- Bulk meal planning
- Calendar integration
- Nutritional goal setting
- Weekly recipe recommendations

## Technical Stack

- **Backend**: Django 4.2
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **API**: JSON REST endpoints

## Getting Started

See README.md for installation and setup instructions.
