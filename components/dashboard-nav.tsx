"use client"

import Link from "next/link"
import { useRouter } from "next/navigation"
import { useAuthContext } from "./auth-provider"

export function DashboardNav() {
  const router = useRouter()
  const { user, logout } = useAuthContext()

  const handleLogout = () => {
    logout()
    router.push("/")
  }

  return (
    <nav className="bg-primary text-primary-foreground shadow-lg">
      <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex gap-6 items-center">
          <Link href="/dashboard" className="text-2xl font-bold hover:opacity-90">
            🍳 Mealy
          </Link>
          <div className="hidden md:flex gap-4">
            <Link href="/dashboard" className="hover:opacity-90">
              Recipes
            </Link>
            <Link href="/meal-plans" className="hover:opacity-90">
              Meal Plans
            </Link>
            <Link href="/shopping-list" className="hover:opacity-90">
              Shopping List
            </Link>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <span className="text-sm">{user?.name}</span>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-primary-foreground text-primary rounded-lg hover:opacity-90 text-sm font-medium"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  )
}
