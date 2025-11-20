// In-memory database with localStorage persistence
import type { User, Recipe, MealPlan, ShoppingListItem } from "./types"

interface Database {
  users: User[]
  recipes: Recipe[]
  mealPlans: MealPlan[]
  shoppingListItems: ShoppingListItem[]
}

const DB_KEY = "mealy_db"

function generateId(): string {
  return Math.random().toString(36).substring(2) + Date.now().toString(36)
}

function loadDatabase(): Database {
  if (typeof window === "undefined") return getDefaultDatabase()

  const stored = localStorage.getItem(DB_KEY)
  if (stored) {
    return JSON.parse(stored)
  }

  return getDefaultDatabase()
}

function saveDatabase(db: Database): void {
  if (typeof window === "undefined") return
  localStorage.setItem(DB_KEY, JSON.stringify(db))
}

function getDefaultDatabase(): Database {
  return {
    users: [
      {
        id: "user1",
        email: "demo@mealy.com",
        name: "Demo User",
      },
    ],
    recipes: [
      {
        id: "recipe1",
        userId: "user1",
        name: "Classic Pasta Carbonara",
        description: "Traditional Italian pasta dish with creamy sauce and bacon",
        ingredients: [
          { id: "ing1", name: "Spaghetti", amount: 400, unit: "g" },
          { id: "ing2", name: "Bacon", amount: 200, unit: "g" },
          { id: "ing3", name: "Eggs", amount: 3, unit: "pcs" },
          { id: "ing4", name: "Parmesan Cheese", amount: 100, unit: "g" },
          { id: "ing5", name: "Black Pepper", amount: 1, unit: "tsp" },
        ],
        instructions: [
          "Cook spaghetti in salted boiling water until al dente",
          "Fry bacon until crispy",
          "Whisk eggs with grated Parmesan cheese",
          "Mix hot pasta with bacon and reserved fat",
          "Add egg mixture and toss quickly",
          "Season with black pepper and serve immediately",
        ],
        prepTime: 10,
        cookTime: 20,
        servings: 4,
        calories: 650,
        dietary: [],
        createdAt: new Date().toISOString(),
      },
      {
        id: "recipe2",
        userId: "user1",
        name: "Buddha Bowl",
        description: "Healthy vegan bowl with quinoa, roasted vegetables, and tahini dressing",
        ingredients: [
          { id: "ing6", name: "Quinoa", amount: 1, unit: "cup" },
          { id: "ing7", name: "Sweet Potato", amount: 2, unit: "pcs" },
          { id: "ing8", name: "Broccoli", amount: 300, unit: "g" },
          { id: "ing9", name: "Chickpeas", amount: 1, unit: "can" },
          { id: "ing10", name: "Tahini", amount: 3, unit: "tbsp" },
          { id: "ing11", name: "Lemon", amount: 1, unit: "pc" },
        ],
        instructions: [
          "Cook quinoa according to package instructions",
          "Roast diced sweet potato and broccoli at 400°F for 25 minutes",
          "Roast chickpeas with spices for 20 minutes",
          "Mix tahini, lemon juice, and water for dressing",
          "Assemble bowl with quinoa, roasted vegetables, and chickpeas",
          "Drizzle with tahini dressing",
        ],
        prepTime: 15,
        cookTime: 30,
        servings: 2,
        calories: 520,
        dietary: ["vegan", "glutenFree"],
        createdAt: new Date().toISOString(),
      },
      {
        id: "recipe3",
        userId: "user1",
        name: "Chocolate Cake",
        description: "Decadent chocolate cake with rich frosting",
        ingredients: [
          { id: "ing12", name: "Flour", amount: 2, unit: "cup" },
          { id: "ing13", name: "Cocoa Powder", amount: 0.75, unit: "cup" },
          { id: "ing14", name: "Sugar", amount: 2, unit: "cup" },
          { id: "ing15", name: "Eggs", amount: 3, unit: "pcs" },
          { id: "ing16", name: "Butter", amount: 0.5, unit: "cup" },
        ],
        instructions: [
          "Preheat oven to 350°F",
          "Mix dry ingredients",
          "Cream butter and sugar",
          "Add eggs one at a time",
          "Combine wet and dry ingredients",
          "Pour into greased pan and bake 30-35 minutes",
        ],
        prepTime: 20,
        cookTime: 35,
        servings: 8,
        calories: 420,
        dietary: [],
        createdAt: new Date().toISOString(),
      },
    ],
    mealPlans: [
      {
        id: "meal1",
        userId: "user1",
        date: new Date().toISOString().split("T")[0],
        mealType: "lunch",
        recipeId: "recipe1",
        createdAt: new Date().toISOString(),
      },
      {
        id: "meal2",
        userId: "user1",
        date: new Date(Date.now() + 86400000).toISOString().split("T")[0],
        mealType: "dinner",
        recipeId: "recipe2",
        createdAt: new Date().toISOString(),
      },
    ],
    shoppingListItems: [
      {
        id: "item1",
        userId: "user1",
        text: "Spaghetti",
        completed: false,
        mealPlanId: "meal1",
        createdAt: new Date().toISOString(),
      },
      {
        id: "item2",
        userId: "user1",
        text: "Bacon",
        completed: false,
        mealPlanId: "meal1",
        createdAt: new Date().toISOString(),
      },
      {
        id: "item3",
        userId: "user1",
        text: "Parmesan Cheese",
        completed: true,
        mealPlanId: "meal1",
        createdAt: new Date().toISOString(),
      },
    ],
  }
}

export const db = {
  // User functions
  getUser(id: string): User | null {
    const database = loadDatabase()
    return database.users.find((u) => u.id === id) || null
  },

  findUserByEmail(email: string): User | null {
    const database = loadDatabase()
    return database.users.find((u) => u.email === email) || null
  },

  createUser(email: string, name: string): User {
    const database = loadDatabase()
    const user: User = {
      id: generateId(),
      email,
      name,
    }
    database.users.push(user)
    saveDatabase(database)
    return user
  },

  // Recipe functions
  getAllRecipes(userId: string): Recipe[] {
    const database = loadDatabase()
    return database.recipes.filter((r) => r.userId === userId)
  },

  getRecipe(id: string): Recipe | null {
    const database = loadDatabase()
    return database.recipes.find((r) => r.id === id) || null
  },

  createRecipe(userId: string, recipe: Omit<Recipe, "id" | "userId" | "createdAt">): Recipe {
    const database = loadDatabase()
    const newRecipe: Recipe = {
      ...recipe,
      id: generateId(),
      userId,
      createdAt: new Date().toISOString(),
    }
    database.recipes.push(newRecipe)
    saveDatabase(database)
    return newRecipe
  },

  updateRecipe(id: string, updates: Partial<Recipe>): Recipe | null {
    const database = loadDatabase()
    const index = database.recipes.findIndex((r) => r.id === id)
    if (index === -1) return null

    database.recipes[index] = { ...database.recipes[index], ...updates }
    saveDatabase(database)
    return database.recipes[index]
  },

  deleteRecipe(id: string): boolean {
    const database = loadDatabase()
    const index = database.recipes.findIndex((r) => r.id === id)
    if (index === -1) return false

    database.recipes.splice(index, 1)
    saveDatabase(database)
    return true
  },

  // Meal Plan functions
  getMealPlans(userId: string, date?: string): MealPlan[] {
    const database = loadDatabase()
    let plans = database.mealPlans.filter((m) => m.userId === userId)
    if (date) {
      plans = plans.filter((m) => m.date === date)
    }
    return plans
  },

  createMealPlan(userId: string, mealPlan: Omit<MealPlan, "id" | "userId" | "createdAt">): MealPlan {
    const database = loadDatabase()
    const newPlan: MealPlan = {
      ...mealPlan,
      id: generateId(),
      userId,
      createdAt: new Date().toISOString(),
    }
    database.mealPlans.push(newPlan)
    saveDatabase(database)
    return newPlan
  },

  deleteMealPlan(id: string): boolean {
    const database = loadDatabase()
    const index = database.mealPlans.findIndex((m) => m.id === id)
    if (index === -1) return false

    database.mealPlans.splice(index, 1)
    saveDatabase(database)
    return true
  },

  // Shopping List functions
  getShoppingList(userId: string): ShoppingListItem[] {
    const database = loadDatabase()
    return database.shoppingListItems.filter((item) => item.userId === userId)
  },

  addShoppingListItem(userId: string, text: string, mealPlanId?: string): ShoppingListItem {
    const database = loadDatabase()
    const item: ShoppingListItem = {
      id: generateId(),
      userId,
      text,
      completed: false,
      mealPlanId,
      createdAt: new Date().toISOString(),
    }
    database.shoppingListItems.push(item)
    saveDatabase(database)
    return item
  },

  toggleShoppingListItem(id: string): ShoppingListItem | null {
    const database = loadDatabase()
    const item = database.shoppingListItems.find((i) => i.id === id)
    if (!item) return null

    item.completed = !item.completed
    saveDatabase(database)
    return item
  },

  deleteShoppingListItem(id: string): boolean {
    const database = loadDatabase()
    const index = database.shoppingListItems.findIndex((i) => i.id === id)
    if (index === -1) return false

    database.shoppingListItems.splice(index, 1)
    saveDatabase(database)
    return true
  },
}
