export interface User {
  id: string
  email: string
  name: string
}

export interface Recipe {
  id: string
  userId: string
  name: string
  description: string
  ingredients: Ingredient[]
  instructions: string[]
  prepTime: number // minutes
  cookTime: number // minutes
  servings: number
  calories: number
  dietary: ("vegan" | "vegetarian" | "glutenFree" | "dairyFree")[]
  createdAt: string
}

export interface Ingredient {
  id: string
  name: string
  amount: number
  unit: string
}

export interface MealPlan {
  id: string
  userId: string
  date: string // YYYY-MM-DD
  mealType: "breakfast" | "lunch" | "dinner" | "snack"
  recipeId: string
  createdAt: string
}

export interface ShoppingListItem {
  id: string
  userId: string
  text: string
  completed: boolean
  mealPlanId?: string
  createdAt: string
}
