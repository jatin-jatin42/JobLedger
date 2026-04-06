import { useState, useEffect, FormEvent } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import {
  getApplication, updateApplication, updateStage, deleteApplication,
  Application, Note,
} from '../api/applications'
import { createNote, deleteNote } from '../api/notes'
import Navbar from '../components/Navbar'
import StageBadge from '../components/StageBadge'
import StageTransitionButtons from '../components/StageTransitionButtons'
import NoteItem from '../components/NoteItem'
import ConfirmModal from '../components/ConfirmModal'
import LoadingSpinner from '../components/LoadingSpinner'
import { Stage } from '../utils/stageConfig'
import { formatDate } from '../utils/formatDate'

export default function ApplicationDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [app, setApp] = useState<Application | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // Edit mode
  const [editing, setEditing] = useState(false)
  const [editForm, setEditForm] = useState<Partial<Application>>({})
  const [editLoading, setEditLoading] = useState(false)
  const [editErrors, setEditErrors] = useState<Record<string, string>>({})

  // Stage transition
  const [stageLoading, setStageLoading] = useState(false)
  const [stageError, setStageError] = useState('')

  // Notes
  const [noteContent, setNoteContent] = useState('')
  const [noteLoading, setNoteLoading] = useState(false)
  const [noteError, setNoteError] = useState('')
  const [deletingNoteId, setDeletingNoteId] = useState<string | null>(null)

  // Delete app modal
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [deleteLoading, setDeleteLoading] = useState(false)

  useEffect(() => {
    if (!id) return
    getApplication(id)
      .then((r: { data: Application }) => { setApp(r.data); setEditForm(r.data) })
      .catch(() => setError('Application not found.'))
      .finally(() => setLoading(false))
  }, [id])

  const handleTransition = async (stage: Stage) => {
    if (!app) return
    setStageLoading(true)
    setStageError('')
    try {
      const r = await updateStage(app.id, stage)
      setApp(r.data)
      setEditForm(r.data)
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { error?: string } } })?.response?.data?.error
      setStageError(msg || 'Stage update failed.')
    } finally {
      setStageLoading(false)
    }
  }

  const handleEditSave = async (e: FormEvent) => {
    e.preventDefault()
    if (!app) return
    setEditErrors({})
    setEditLoading(true)
    try {
      const payload: Record<string, unknown> = {
        company_name: editForm.company_name,
        role_title: editForm.role_title,
        job_url: editForm.job_url || null,
        location: editForm.location || null,
        salary_min: editForm.salary_min ?? null,
        salary_max: editForm.salary_max ?? null,
        applied_date: editForm.applied_date,
      }
      const r = await updateApplication(app.id, payload)
      setApp(r.data)
      setEditing(false)
    } catch (err: unknown) {
      const errData = (err as { response?: { data?: { error?: unknown } } })?.response?.data?.error
      if (typeof errData === 'object' && errData !== null) {
        const flat: Record<string, string> = {}
        Object.entries(errData as Record<string, unknown>).forEach(([k, v]) => {
          flat[k] = Array.isArray(v) ? v.join(', ') : String(v)
        })
        setEditErrors(flat)
      } else {
        setEditErrors({ _general: String(errData || 'Update failed.') })
      }
    } finally {
      setEditLoading(false)
    }
  }

  const handleAddNote = async (e: FormEvent) => {
    e.preventDefault()
    if (!app || !noteContent.trim()) return
    setNoteLoading(true)
    setNoteError('')
    try {
      const r = await createNote(app.id, noteContent)
      setApp((prev: Application | null) => prev ? { ...prev, notes: [...(prev.notes || []), r.data] } : prev)
      setNoteContent('')
    } catch {
      setNoteError('Failed to add note.')
    } finally {
      setNoteLoading(false)
    }
  }

  const handleDeleteNote = async (noteId: string) => {
    if (!app) return
    setDeletingNoteId(noteId)
    try {
      await deleteNote(app.id, noteId)
      setApp((prev: Application | null) => prev ? { ...prev, notes: (prev.notes || []).filter((n: Note) => n.id !== noteId) } : prev)
    } catch {
      // silently fail — note stays visible
    } finally {
      setDeletingNoteId(null)
    }
  }

  const handleDeleteApp = async () => {
    if (!app) return
    setDeleteLoading(true)
    try {
      await deleteApplication(app.id)
      navigate('/applications')
    } catch {
      setDeleteLoading(false)
      setShowDeleteModal(false)
    }
  }

  if (loading) return (
    <div className="min-h-screen bg-slate-50"><Navbar />
      <div className="flex justify-center py-20"><LoadingSpinner size="lg" /></div>
    </div>
  )
  if (error || !app) return (
    <div className="min-h-screen bg-slate-50"><Navbar />
      <div className="max-w-3xl mx-auto px-4 py-10">
        <div className="card text-center">
          <p className="text-slate-500">{error || 'Application not found.'}</p>
          <Link to="/applications" className="btn-primary mt-4 inline-flex">Back to applications</Link>
        </div>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />

      <ConfirmModal
        isOpen={showDeleteModal}
        title="Delete application"
        message={<>Are you sure you want to delete the application for <strong>{app.company_name}</strong>? This cannot be undone.</>}
        confirmLabel={deleteLoading ? 'Deleting…' : 'Delete'}
        danger
        onConfirm={handleDeleteApp}
        onCancel={() => setShowDeleteModal(false)}
      />

      <div className="max-w-3xl mx-auto px-4 sm:px-6 py-8 space-y-6">
        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <Link to="/applications" className="text-sm text-indigo-600 hover:underline">← Applications</Link>
            <h1 className="text-2xl font-bold text-slate-900 mt-1">{app.company_name}</h1>
            <p className="text-slate-600">{app.role_title}</p>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <StageBadge stage={app.stage} />
            <button
              id="edit-application-btn"
              onClick={() => { setEditing(!editing); setEditErrors({}) }}
              className="btn-secondary text-xs"
            >
              {editing ? 'Cancel' : 'Edit'}
            </button>
            <button
              id="delete-application-btn"
              onClick={() => setShowDeleteModal(true)}
              className="btn-danger text-xs"
            >
              Delete
            </button>
          </div>
        </div>

        {/* Details / Edit form */}
        <div className="card">
          {editing ? (
            <form onSubmit={handleEditSave} id="edit-application-form" className="space-y-4">
              <h2 className="font-semibold text-slate-800">Edit Application</h2>
              {editErrors._general && <p className="form-error">{editErrors._general}</p>}
              <div className="grid sm:grid-cols-2 gap-4">
                {[
                  { id: 'company_name', label: 'Company name', required: true },
                  { id: 'role_title', label: 'Role title', required: true },
                ].map(({ id: fid, label, required }) => (
                  <div key={fid}>
                    <label htmlFor={`edit-${fid}`} className="label">{label}</label>
                    <input
                      id={`edit-${fid}`}
                      value={(editForm[fid as keyof Application] as string) || ''}
                      onChange={(e) => setEditForm((f) => ({ ...f, [fid]: e.target.value }))}
                      className="input" required={required}
                    />
                    {editErrors[fid] && <p className="form-error">{editErrors[fid]}</p>}
                  </div>
                ))}
              </div>
              <div>
                <label htmlFor="edit-job_url" className="label">Job URL</label>
                <input id="edit-job_url" value={editForm.job_url || ''} onChange={(e) => setEditForm((f) => ({ ...f, job_url: e.target.value }))} className="input" />
              </div>
              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="edit-location" className="label">Location</label>
                  <input id="edit-location" value={editForm.location || ''} onChange={(e) => setEditForm((f) => ({ ...f, location: e.target.value }))} className="input" />
                </div>
                <div>
                  <label htmlFor="edit-applied_date" className="label">Applied date</label>
                  <input id="edit-applied_date" type="date" value={editForm.applied_date || ''} onChange={(e) => setEditForm((f) => ({ ...f, applied_date: e.target.value }))} className="input" max={new Date().toISOString().split('T')[0]} />
                  {editErrors.applied_date && <p className="form-error">{editErrors.applied_date}</p>}
                </div>
              </div>
              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="edit-salary_min" className="label">Salary min</label>
                  <input id="edit-salary_min" type="number" min={0} value={editForm.salary_min ?? ''} onChange={(e) => setEditForm((f) => ({ ...f, salary_min: e.target.value ? Number(e.target.value) : undefined }))} className="input" />
                  {editErrors.salary_min && <p className="form-error">{editErrors.salary_min}</p>}
                </div>
                <div>
                  <label htmlFor="edit-salary_max" className="label">Salary max</label>
                  <input id="edit-salary_max" type="number" min={0} value={editForm.salary_max ?? ''} onChange={(e) => setEditForm((f) => ({ ...f, salary_max: e.target.value ? Number(e.target.value) : undefined }))} className="input" />
                </div>
              </div>
              <div className="flex justify-end gap-3 pt-2">
                <button type="button" onClick={() => setEditing(false)} className="btn-secondary">Cancel</button>
                <button id="edit-save-btn" type="submit" disabled={editLoading} className="btn-primary">
                  {editLoading ? <><LoadingSpinner size="sm" /> Saving…</> : 'Save changes'}
                </button>
              </div>
            </form>
          ) : (
            <div className="grid sm:grid-cols-2 gap-x-8 gap-y-4">
              {[
                { label: 'Company', value: app.company_name },
                { label: 'Role', value: app.role_title },
                { label: 'Location', value: app.location || '—' },
                { label: 'Applied', value: formatDate(app.applied_date) },
                {
                  label: 'Salary',
                  value: app.salary_min || app.salary_max
                    ? [app.salary_min, app.salary_max].filter(Boolean).map((v) => v?.toLocaleString()).join(' – ')
                    : '—',
                },
                {
                  label: 'Job URL',
                  value: app.job_url
                    ? <a href={app.job_url} target="_blank" rel="noopener noreferrer" className="text-indigo-600 hover:underline truncate block max-w-xs">View posting ↗</a>
                    : '—',
                },
              ].map(({ label, value }) => (
                <div key={label}>
                  <p className="text-xs font-medium text-slate-400 uppercase tracking-wide">{label}</p>
                  <p className="mt-0.5 text-sm text-slate-800">{value}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Stage transition */}
        <div className="card">
          <h2 className="font-semibold text-slate-800 mb-3">Advance Stage</h2>
          <div className="flex items-center gap-3 mb-3">
            <span className="text-sm text-slate-500">Current:</span>
            <StageBadge stage={app.stage} />
          </div>
          {stageError && (
            <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-2 mb-3">{stageError}</div>
          )}
          <StageTransitionButtons
            currentStage={app.stage}
            onTransition={handleTransition}
            loading={stageLoading}
          />
        </div>

        {/* Notes */}
        <div className="card">
          <h2 className="font-semibold text-slate-800 mb-4">Notes ({app.notes?.length ?? 0})</h2>

          {/* Add note form */}
          <form onSubmit={handleAddNote} id="add-note-form" className="mb-5">
            <textarea
              id="note-content-input"
              value={noteContent}
              onChange={(e) => setNoteContent(e.target.value)}
              placeholder="Add a note…"
              rows={3}
              className="input resize-none"
            />
            {noteError && <p className="form-error">{noteError}</p>}
            <div className="flex justify-end mt-2">
              <button
                id="add-note-submit-btn"
                type="submit"
                disabled={noteLoading || !noteContent.trim()}
                className="btn-primary text-sm"
              >
                {noteLoading ? <><LoadingSpinner size="sm" /> Adding…</> : 'Add Note'}
              </button>
            </div>
          </form>

          {/* Notes list */}
          {!app.notes?.length ? (
            <p className="text-sm text-slate-400 text-center py-6 italic">No notes yet. Add one above.</p>
          ) : (
            <div className="space-y-3">
              {[...(app.notes || [])].reverse().map((note) => (
                <NoteItem
                  key={note.id}
                  note={note}
                  onDelete={handleDeleteNote}
                  deleting={deletingNoteId === note.id}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
