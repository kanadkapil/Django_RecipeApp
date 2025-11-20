interface TokenPayload {
  userId: string
  email: string
  iat: number
  exp: number
}

const SECRET = "mealy-secret-key-change-in-production"

export function generateToken(userId: string, email: string): string {
  const payload = {
    userId,
    email,
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + 86400 * 7, // 7 days
  }

  return btoa(JSON.stringify(payload))
}

export function verifyToken(token: string): TokenPayload | null {
  try {
    const decoded = JSON.parse(atob(token)) as TokenPayload
    const now = Math.floor(Date.now() / 1000)

    if (decoded.exp < now) {
      return null
    }

    return decoded
  } catch {
    return null
  }
}

export function getStoredToken(): string | null {
  if (typeof window === "undefined") return null
  return localStorage.getItem("auth_token")
}

export function setStoredToken(token: string): void {
  if (typeof window === "undefined") return
  localStorage.setItem("auth_token", token)
}

export function clearStoredToken(): void {
  if (typeof window === "undefined") return
  localStorage.removeItem("auth_token")
}

export function getCurrentUser(): TokenPayload | null {
  const token = getStoredToken()
  if (!token) return null
  return verifyToken(token)
}
