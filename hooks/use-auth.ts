"use client"

import { useState, useEffect, useCallback } from "react"
import { getCurrentUser, setStoredToken, clearStoredToken, generateToken } from "@/lib/auth"
import { db } from "@/lib/db"
import type { User } from "@/lib/types"

interface TokenPayload {
  userId: string
  email: string
}

export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const currentUser = getCurrentUser()
    if (currentUser) {
      const userData = db.getUser(currentUser.userId)
      setUser(userData)
    }
    setLoading(false)
  }, [])

  const login = useCallback((email: string, password: string) => {
    // Simple password check (password is email in demo)
    const existingUser = db.findUserByEmail(email)

    if (!existingUser) {
      throw new Error("User not found")
    }

    const token = generateToken(existingUser.id, existingUser.email)
    setStoredToken(token)
    setUser(existingUser)

    return existingUser
  }, [])

  const signup = useCallback((email: string, name: string, password: string) => {
    const existingUser = db.findUserByEmail(email)

    if (existingUser) {
      throw new Error("User already exists")
    }

    const newUser = db.createUser(email, name)
    const token = generateToken(newUser.id, newUser.email)
    setStoredToken(token)
    setUser(newUser)

    return newUser
  }, [])

  const logout = useCallback(() => {
    clearStoredToken()
    setUser(null)
  }, [])

  return {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    signup,
    logout,
  }
}
