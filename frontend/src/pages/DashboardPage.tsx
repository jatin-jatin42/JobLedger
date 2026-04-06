import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getDashboard } from '../api/dashboard'
import { Application } from '../api/applications'
import { useAuth } from '../context/AuthContext'
import Navbar from '../components/Navbar'
import StageBadge from '../components/StageBadge'
import LoadingSpinner from '../components/LoadingSpinner'
import { STAGE_CONFIG, ALL_STAGES, Stage } from '../utils/stageConfig'
import { formatRelative } from '../utils/formatDate'

interface DashboardData {
  total: number
  by_stage: Record<string, number>
  recent_activity: Application[]
}

export default function DashboardPage() {
  const { user } = useAuth()
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    getDashboard()
      .then((r) => setData(r.data))
      .catch(() => setError('Failed to load dashboard.'))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-slate-900">
            Welcome back, {user?.full_name?.split(' ')[0]} 👋
          </h1>
          <p className="text-slate-500 mt-1">Here's your job search at a glance.</p>
        </div>

        {loading && (
          <div className="flex justify-center py-16"><LoadingSpinner size="lg" /></div>
        )}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4">{error}</div>
        )}

        {data && (
          <>
            {/* Total card */}
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-7 gap-3 mb-8">
              <div className="col-span-2 sm:col-span-1 bg-indigo-600 text-white rounded-xl p-4 shadow-sm">
                <p className="text-indigo-200 text-xs font-medium uppercase tracking-wide">Total</p>
                <p className="text-4xl font-bold mt-1">{data.total}</p>
                <p className="text-indigo-200 text-xs mt-1">Applications</p>
              </div>

              {ALL_STAGES.map((stage) => {
                const cfg = STAGE_CONFIG[stage as Stage]
                const count = data.by_stage[stage] ?? 0
                return (
                  <div key={stage} className={`rounded-xl p-4 border ${cfg.bg} ${cfg.ring} ring-1`}>
                    <p className={`text-xs font-medium uppercase tracking-wide ${cfg.color}`}>
                      {cfg.label}
                    </p>
                    <p className={`text-3xl font-bold mt-1 ${cfg.color}`}>{count}</p>
                  </div>
                )
              })}
            </div>

            {/* Recent activity */}
            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-slate-800">Recent Activity</h2>
                <Link to="/applications" className="text-sm text-indigo-600 hover:underline">
                  View all →
                </Link>
              </div>

              {data.recent_activity.length === 0 ? (
                <div className="text-center py-12 text-slate-400">
                  <p className="text-4xl mb-3">📭</p>
                  <p className="font-medium">No applications yet</p>
                  <Link to="/applications/new" className="btn-primary mt-4 inline-flex">
                    Add your first application
                  </Link>
                </div>
              ) : (
                <div className="divide-y divide-slate-100">
                  {data.recent_activity.map((app) => (
                    <Link
                      key={app.id}
                      to={`/applications/${app.id}`}
                      className="flex items-center justify-between py-3 hover:bg-slate-50 -mx-2 px-2 rounded-lg transition-colors"
                    >
                      <div>
                        <p className="font-medium text-slate-800 text-sm">{app.company_name}</p>
                        <p className="text-xs text-slate-500">{app.role_title}</p>
                      </div>
                      <div className="flex items-center gap-3">
                        <StageBadge stage={app.stage} size="sm" />
                        <span className="text-xs text-slate-400 hidden sm:block">
                          {formatRelative(app.updated_at)}
                        </span>
                      </div>
                    </Link>
                  ))}
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  )
}
