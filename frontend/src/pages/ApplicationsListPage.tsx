import { useState, useEffect, useCallback } from 'react'
import { Link } from 'react-router-dom'
import { getApplications, Application } from '../api/applications'
import Navbar from '../components/Navbar'
import ApplicationCard from '../components/ApplicationCard'
import LoadingSpinner from '../components/LoadingSpinner'
import { ALL_STAGES, STAGE_CONFIG, Stage } from '../utils/stageConfig'

export default function ApplicationsListPage() {
  const [applications, setApplications] = useState<Application[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [stageFilter, setStageFilter] = useState('')
  const [search, setSearch] = useState('')
  const [sortBy, setSortBy] = useState('updated_at')
  const [order, setOrder] = useState('desc')

  const fetchApps = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const r = await getApplications({
        ...(stageFilter && { stage: stageFilter }),
        ...(search && { search }),
        sort_by: sortBy,
        order,
      })
      setApplications(r.data)
      setTotal(r.total)
    } catch {
      setError('Failed to load applications.')
    } finally {
      setLoading(false)
    }
  }, [stageFilter, search, sortBy, order])

  useEffect(() => { fetchApps() }, [fetchApps])

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">Applications</h1>
            <p className="text-slate-500 text-sm mt-1">{total} total</p>
          </div>
          <Link to="/applications/new" id="new-application-btn" className="btn-primary">
            + New Application
          </Link>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-3 mb-6">
          {/* Search */}
          <input
            id="search-input"
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search company or role…"
            className="input max-w-xs"
          />

          {/* Stage filter tabs */}
          <div className="flex flex-wrap gap-1.5">
            <button
              onClick={() => setStageFilter('')}
              className={`text-xs px-3 py-1.5 rounded-full border transition-all font-medium ${  stageFilter === '' ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-slate-600 border-slate-300 hover:border-indigo-300'}`}
            >
              All
            </button>
            {ALL_STAGES.map((stage) => {
              const cfg = STAGE_CONFIG[stage as Stage]
              const active = stageFilter === stage
              return (
                <button
                  key={stage}
                  id={`filter-${stage.toLowerCase()}`}
                  onClick={() => setStageFilter(stage)}
                  className={`text-xs px-3 py-1.5 rounded-full border transition-all font-medium ${active ? `${cfg.bg} ${cfg.color} ${cfg.ring} ring-1` : 'bg-white text-slate-600 border-slate-300 hover:border-slate-400'}`}
                >
                  {cfg.label}
                </button>
              )
            })}
          </div>

          {/* Sort */}
          <select
            id="sort-select"
            value={`${sortBy}:${order}`}
            onChange={(e) => {
              const [s, o] = e.target.value.split(':')
              setSortBy(s)
              setOrder(o)
            }}
            className="input max-w-[180px] text-sm"
          >
            <option value="updated_at:desc">Recently updated</option>
            <option value="updated_at:asc">Oldest updated</option>
            <option value="applied_date:desc">Applied (newest)</option>
            <option value="applied_date:asc">Applied (oldest)</option>
            <option value="company_name:asc">Company A–Z</option>
            <option value="company_name:desc">Company Z–A</option>
          </select>
        </div>

        {/* Content */}
        {loading && <div className="flex justify-center py-16"><LoadingSpinner size="lg" /></div>}
        {error && <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4">{error}</div>}

        {!loading && !error && applications.length === 0 && (
          <div className="text-center py-20 text-slate-400">
            <p className="text-5xl mb-4">🔍</p>
            <p className="font-medium text-lg">No applications found</p>
            <p className="text-sm mt-1">Try adjusting your filters or add a new application.</p>
            <Link to="/applications/new" className="btn-primary mt-6 inline-flex">
              + Add Application
            </Link>
          </div>
        )}

        {!loading && applications.length > 0 && (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {applications.map((app) => (
              <ApplicationCard key={app.id} application={app} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
