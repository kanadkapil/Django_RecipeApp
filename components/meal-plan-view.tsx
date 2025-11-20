"use client"

import { useState } from "react"
import Link from "next/link"
import { useAuthContext } from "./auth-provider"
import { db } from "@/lib/db"

export function MealPlanView() {
  const { user } = useAuthContext()
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split("T")[0])

  if (!user) return null

  const mealPlans = db.getMealPlans(user.id, selectedDate)
  const recipes = db.getAllRecipes(user.id)

  const mealsWithRecipes = mealPlans
    .map((meal) => ({
      ...meal,
      recipe: recipes.find((r) => r.id === meal.recipeId),
    }))
    .filter((m) => m.recipe)

  const handleDeleteMealPlan = (id: string) => {
    if (db.deleteMealPlan(id)) {
      window.location.reload()
    }
  }

  const totalCalories = mealsWithRecipes.reduce((sum, meal) => sum + (meal.recipe?.calories || 0), 0)

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <label className="block text-sm font-medium mb-2 text-foreground">Select Date</label>
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="px-4 py-2 border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-background text-foreground"
          />
        </div>
        <Link
          href="/meal-plans/new"
          className="px-6 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90 font-semibold h-fit"
        >
          + Add Meal
        </Link>
      </div>

      {mealsWithRecipes.length > 0 && (
        <div className="bg-primary/10 border border-primary/20 rounded-lg p-4">
          <p className="text-sm text-muted-foreground">Total Calories for {selectedDate}</p>
          <p className="text-3xl font-bold text-primary">{totalCalories} kcal</p>
        </div>
      )}

      <div className="grid gap-4">
        {mealsWithRecipes.length === 0 ? (
          <p className="text-center py-8 text-muted-foreground">No meals planned for this date</p>
        ) : (
          mealsWithRecipes.map((meal) => (
            <div key={meal.id} className="p-4 bg-card border border-border rounded-lg">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <p className="text-xs text-muted-foreground uppercase font-semibold">{meal.mealType}</p>
                  <h3 className="text-lg font-semibold text-card-foreground">{meal.recipe?.name}</h3>
                </div>
                <button
                  onClick={() => handleDeleteMealPlan(meal.id)}
                  className="text-destructive hover:opacity-70 text-sm"
                >
                  Delete
                </button>
              </div>
              <p className="text-sm text-muted-foreground mb-2">{meal.recipe?.description}</p>
              <p className="text-sm font-medium text-primary">{meal.recipe?.calories} kcal per serving</p>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
