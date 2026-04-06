import { Link } from 'react-router-dom'
import { Application } from '../api/applications'
import StageBadge from './StageBadge'
import { formatDate, formatRelative } from '../utils/formatDate'

interface ApplicationCardProps {
  application: Application
}

export default function ApplicationCard({ application: app }: ApplicationCardProps) {
  return (
    <Link
      to={`/applications/${app.id}`}
      id={`app-card-${app.id}`}
      className="block bg-white rounded-xl border border-slate-200 p-4 hover:border-indigo-300 hover:shadow-md transition-all duration-150 group"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="font-semibold text-slate-900 group-hover:text-indigo-600 transition-colors truncate">
            {app.company_name}
          </p>
          <p className="text-sm text-slate-600 truncate mt-0.5">{app.role_title}</p>
          {app.location && (
            <p className="text-xs text-slate-400 mt-1">📍 {app.location}</p>
          )}
        </div>
        <StageBadge stage={app.stage} />
      </div>

      <div className="flex items-center justify-between mt-3 text-xs text-slate-400">
        <span>Applied {formatDate(app.applied_date)}</span>
        <span>Updated {formatRelative(app.updated_at)}</span>
      </div>

      {(app.salary_min || app.salary_max) && (
        <p className="text-xs text-slate-500 mt-2">
          💰{' '}
          {app.salary_min && app.salary_max
            ? `${app.salary_min.toLocaleString()} – ${app.salary_max.toLocaleString()}`
            : app.salary_min?.toLocaleString() ?? app.salary_max?.toLocaleString()}
        </p>
      )}
    </Link>
  )
}
