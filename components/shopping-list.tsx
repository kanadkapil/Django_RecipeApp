"use client"

import type React from "react"

import { useState } from "react"
import { db } from "@/lib/db"
import { useAuthContext } from "./auth-provider"
import type { ShoppingListItem } from "@/lib/types"

interface ShoppingListProps {
  items: ShoppingListItem[]
  onUpdate?: () => void
}

export function ShoppingList({ items: initialItems, onUpdate }: ShoppingListProps) {
  const [items, setItems] = useState(initialItems)
  const [newItem, setNewItem] = useState("")
  const { user } = useAuthContext()

  if (!user) return null

  const handleAddItem = (e: React.FormEvent) => {
    e.preventDefault()
    if (!newItem.trim()) return

    const item = db.addShoppingListItem(user.id, newItem)
    setItems([...items, item])
    setNewItem("")
    onUpdate?.()
  }

  const handleToggle = (id: string) => {
    const updated = db.toggleShoppingListItem(id)
    if (updated) {
      setItems(items.map((item) => (item.id === id ? updated : item)))
      onUpdate?.()
    }
  }

  const handleDelete = (id: string) => {
    if (db.deleteShoppingListItem(id)) {
      setItems(items.filter((item) => item.id !== id))
      onUpdate?.()
    }
  }

  const completedCount = items.filter((item) => item.completed).length

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-foreground">Shopping List</h2>
        <span className="text-sm text-muted-foreground">
          {completedCount}/{items.length} completed
        </span>
      </div>

      <form onSubmit={handleAddItem} className="flex gap-2">
        <input
          type="text"
          value={newItem}
          onChange={(e) => setNewItem(e.target.value)}
          placeholder="Add item..."
          className="flex-1 px-4 py-2 border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-background text-foreground"
        />
        <button type="submit" className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90">
          Add
        </button>
      </form>

      <div className="space-y-2">
        {items.length === 0 ? (
          <p className="text-center py-8 text-muted-foreground">No items yet</p>
        ) : (
          items.map((item) => (
            <div key={item.id} className="flex items-center gap-3 p-3 bg-card border border-border rounded-lg">
              <input
                type="checkbox"
                checked={item.completed}
                onChange={() => handleToggle(item.id)}
                className="w-5 h-5 cursor-pointer"
              />
              <span className={`flex-1 ${item.completed ? "line-through text-muted-foreground" : "text-foreground"}`}>
                {item.text}
              </span>
              <button onClick={() => handleDelete(item.id)} className="text-destructive hover:opacity-70 text-sm">
                Delete
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
