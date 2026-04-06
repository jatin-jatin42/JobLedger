import { useState, FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { register as apiRegister } from '../api/auth'
import { useAuth } from '../context/AuthContext'
import LoadingSpinner from '../components/LoadingSpinner'
import { login as apiLogin } from '../api/auth'

export default function RegisterPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | Record<string, unknown>>('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await apiRegister({ email, password, full_name: fullName })
      // Auto-login after register
      const loginResp = await apiLogin({ email, password })
      login(loginResp.data.access_token, loginResp.data.user)
      navigate('/dashboard')
    } catch (err: unknown) {
      const data = (err as { response?: { data?: { error?: unknown } } })?.response?.data
      setError((data?.error as string) || 'Registration failed.')
    } finally {
      setLoading(false)
    }
  }

  const renderError = () => {
    if (!error) return null
    if (typeof error === 'string') {
      return <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3 mb-4">{error}</div>
    }
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3 mb-4">
        {Object.entries(error).map(([field, msgs]) => (
          <p key={field}><strong>{field}</strong>: {Array.isArray(msgs) ? msgs.join(', ') : String(msgs)}</p>
        ))}
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-slate-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <span className="text-5xl">📋</span>
          <h1 className="text-3xl font-bold text-slate-900 mt-3">JobLedger</h1>
          <p className="text-slate-500 mt-1 text-sm">Start tracking your job search today.</p>
        </div>

        <div className="card shadow-lg">
          <h2 className="text-xl font-semibold text-slate-800 mb-6">Create your account</h2>

          {renderError()}

          <form onSubmit={handleSubmit} className="space-y-4" id="register-form">
            <div>
              <label htmlFor="register-name" className="label">Full name</label>
              <input
                id="register-name"
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="input"
                placeholder="Jane Smith"
                required
                autoComplete="name"
              />
            </div>
            <div>
              <label htmlFor="register-email" className="label">Email address</label>
              <input
                id="register-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input"
                placeholder="you@example.com"
                required
                autoComplete="email"
              />
            </div>
            <div>
              <label htmlFor="register-password" className="label">Password</label>
              <input
                id="register-password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input"
                placeholder="At least 8 characters"
                required
                minLength={8}
                autoComplete="new-password"
              />
            </div>
            <button
              id="register-submit-btn"
              type="submit"
              disabled={loading}
              className="btn-primary w-full justify-center py-2.5 mt-2"
            >
              {loading ? <><LoadingSpinner size="sm" /> Creating account…</> : 'Create account'}
            </button>
          </form>

          <p className="text-center text-sm text-slate-500 mt-6">
            Already have an account?{' '}
            <Link to="/login" className="text-indigo-600 font-medium hover:underline">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
