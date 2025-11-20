"use client"

import { useState } from "react"
import { useAuthContext } from "./auth-provider"
import { db } from "@/lib/db"
import { RecipeCard } from "./recipe-card"
import Link from "next/link"

export function RecipeList() {
  const { user } = useAuthContext()
  const [dietaryFilter, setDietaryFilter] = useState<string>("all")

  if (!user) return null

  const recipes = db.getAllRecipes(user.id)

  const filtered = dietaryFilter === "all" ? recipes : recipes.filter((r) => r.dietary.includes(dietaryFilter as any))

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div className="flex gap-2">
          <select
            value={dietaryFilter}
            onChange={(e) => setDietaryFilter(e.target.value)}
            className="px-4 py-2 border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-background text-foreground"
          >
            <option value="all">All Recipes</option>
            <option value="vegan">Vegan</option>
            <option value="vegetarian">Vegetarian</option>
            <option value="glutenFree">Gluten Free</option>
            <option value="dairyFree">Dairy Free</option>
          </select>
        </div>

        <Link
          href="/recipes/new"
          className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90 font-medium"
        >
          + New Recipe
        </Link>
      </div>

      {filtered.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-muted-foreground mb-4">No recipes found</p>
          <Link href="/recipes/new" className="text-primary hover:underline">
            Create your first recipe
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((recipe) => (
            <RecipeCard key={recipe.id} recipe={recipe} />
          ))}
        </div>
      )}
    </div>
  )
}
