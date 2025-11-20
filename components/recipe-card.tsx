import Link from "next/link"
import type { Recipe } from "@/lib/types"

interface RecipeCardProps {
  recipe: Recipe
}

export function RecipeCard({ recipe }: RecipeCardProps) {
  const totalTime = recipe.prepTime + recipe.cookTime

  return (
    <Link href={`/recipes/${recipe.id}`}>
      <div className="bg-card border border-border rounded-lg p-4 hover:shadow-lg transition-shadow cursor-pointer">
        <h3 className="font-semibold text-lg text-card-foreground mb-2">{recipe.name}</h3>
        <p className="text-sm text-muted-foreground mb-4 line-clamp-2">{recipe.description}</p>

        <div className="flex gap-4 text-xs text-muted-foreground mb-3">
          <div>⏱️ {totalTime} min</div>
          <div>👥 {recipe.servings} servings</div>
        </div>

        {recipe.dietary.length > 0 && (
          <div className="flex gap-2 flex-wrap">
            {recipe.dietary.map((diet) => (
              <span key={diet} className="text-xs px-2 py-1 bg-accent text-accent-foreground rounded-full">
                {diet}
              </span>
            ))}
          </div>
        )}
      </div>
    </Link>
  )
}
