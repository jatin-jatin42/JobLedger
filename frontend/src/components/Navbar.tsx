import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const isActive = (path: string) =>
    location.pathname === path || location.pathname.startsWith(path + '/')
      ? 'text-indigo-600 font-semibold'
      : 'text-slate-600 hover:text-slate-900'

  return (
    <nav className="bg-white border-b border-slate-200 sticky top-0 z-40">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/dashboard" className="flex items-center gap-2 font-bold text-lg text-indigo-600">
            <span className="text-2xl">📋</span>
            <span>JobLedger</span>
          </Link>

          {/* Nav links */}
          <div className="flex items-center gap-6">
            <Link to="/dashboard" className={`text-sm transition-colors ${isActive('/dashboard')}`}>
              Dashboard
            </Link>
            <Link to="/applications" className={`text-sm transition-colors ${isActive('/applications')}`}>
              Applications
            </Link>
          </div>

          {/* User + logout */}
          <div className="flex items-center gap-4">
            <span className="text-sm text-slate-500 hidden sm:block">
              {user?.full_name}
            </span>
            <button
              onClick={handleLogout}
              className="btn-secondary text-xs px-3 py-1.5"
              id="navbar-logout-btn"
            >
              Sign out
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
