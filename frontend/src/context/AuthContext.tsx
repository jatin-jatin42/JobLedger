import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { getMe } from '../api/auth'

export interface User {
  id: string
  email: string
  full_name: string
  created_at: string
}

interface AuthContextType {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (token: string, user: User) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(localStorage.getItem('access_token'))
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const verifyToken = async () => {
      const stored = localStorage.getItem('access_token')
      if (!stored) { setIsLoading(false); return }
      try {
        const resp = await getMe()
        setUser(resp.data)
      } catch {
        localStorage.removeItem('access_token')
        setToken(null)
        setUser(null)
      } finally {
        setIsLoading(false)
      }
    }
    verifyToken()
  }, [])

  const login = (newToken: string, newUser: User) => {
    localStorage.setItem('access_token', newToken)
    setToken(newToken)
    setUser(newUser)
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, token, isAuthenticated: !!token && !!user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
