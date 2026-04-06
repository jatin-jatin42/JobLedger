import { useState, FormEvent } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { createApplication } from '../api/applications'
import Navbar from '../components/Navbar'
import LoadingSpinner from '../components/LoadingSpinner'

export default function NewApplicationPage() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [form, setForm] = useState({
    company_name: '', role_title: '', job_url: '',
    location: '', salary_min: '', salary_max: '',
    applied_date: new Date().toISOString().split('T')[0],
  })

  const set = (field: string) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((f) => ({ ...f, [field]: e.target.value }))

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setErrors({})
    setLoading(true)
    try {
      const payload = {
        company_name: form.company_name,
        role_title: form.role_title,
        ...(form.job_url && { job_url: form.job_url }),
        ...(form.location && { location: form.location }),
        ...(form.salary_min && { salary_min: Number(form.salary_min) }),
        ...(form.salary_max && { salary_max: Number(form.salary_max) }),
        applied_date: form.applied_date,
      }
      const resp = await createApplication(payload)
      navigate(`/applications/${resp.data.id}`)
    } catch (err: unknown) {
      const errData = (err as { response?: { data?: { error?: unknown } } })?.response?.data?.error
      if (typeof errData === 'object' && errData !== null) {
        const flat: Record<string, string> = {}
        Object.entries(errData).forEach(([k, v]) => {
          flat[k] = Array.isArray(v) ? v.join(', ') : String(v)
        })
        setErrors(flat)
      } else {
        setErrors({ _general: String(errData || 'Failed to create application.') })
      }
    } finally {
      setLoading(false)
    }
  }

  const renderField = (id: string, label: string, required = false) => (
    <div key={id}>
      <label htmlFor={id} className="label">{label}{required && <span className="text-red-500 ml-0.5">*</span>}</label>
      <input id={id} value={form[id as keyof typeof form]} onChange={set(id)} className="input" required={required} />
      {errors[id] && <p className="form-error">{errors[id]}</p>}
    </div>
  )

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <div className="max-w-2xl mx-auto px-4 sm:px-6 py-8">
        <div className="mb-6">
          <Link to="/applications" className="text-sm text-indigo-600 hover:underline">← Back to applications</Link>
          <h1 className="text-2xl font-bold text-slate-900 mt-2">New Application</h1>
        </div>

        <div className="card">
          {errors._general && (
            <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3 mb-5">
              {errors._general}
            </div>
          )}

          <form onSubmit={handleSubmit} id="new-application-form" className="space-y-5">
            <div className="grid sm:grid-cols-2 gap-4">
              {renderField("company_name", "Company name", true)}
              {renderField("role_title", "Role / Job title", true)}
            </div>
            {renderField("job_url", "Job posting URL")}
            <div className="grid sm:grid-cols-2 gap-4">
              {renderField("location", "Location")}
              <div>
                <label htmlFor="applied_date" className="label">Applied date</label>
                <input id="applied_date" type="date" value={form.applied_date} onChange={set('applied_date')}
                  className="input" max={new Date().toISOString().split('T')[0]} />
                {errors.applied_date && <p className="form-error">{errors.applied_date}</p>}
              </div>
            </div>
            <div className="grid sm:grid-cols-2 gap-4">
              <div>
                <label htmlFor="salary_min" className="label">Salary min (local currency)</label>
                <input id="salary_min" type="number" min={0} value={form.salary_min} onChange={set('salary_min')} className="input" placeholder="e.g. 80000" />
                {errors.salary_min && <p className="form-error">{errors.salary_min}</p>}
              </div>
              <div>
                <label htmlFor="salary_max" className="label">Salary max</label>
                <input id="salary_max" type="number" min={0} value={form.salary_max} onChange={set('salary_max')} className="input" placeholder="e.g. 120000" />
                {errors.salary_max && <p className="form-error">{errors.salary_max}</p>}
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-2">
              <Link to="/applications" className="btn-secondary">Cancel</Link>
              <button id="create-application-submit" type="submit" disabled={loading} className="btn-primary">
                {loading ? <><LoadingSpinner size="sm" /> Creating…</> : 'Create Application'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
