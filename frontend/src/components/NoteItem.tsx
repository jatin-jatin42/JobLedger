import { Note } from '../api/applications'
import { formatDateTime } from '../utils/formatDate'

interface NoteItemProps {
  note: Note
  onDelete: (noteId: string) => void
  deleting?: boolean
}

export default function NoteItem({ note, onDelete, deleting }: NoteItemProps) {
  return (
    <div className="bg-slate-50 rounded-lg border border-slate-200 p-4 group">
      <p className="text-sm text-slate-700 whitespace-pre-wrap">{note.content}</p>
      <div className="flex items-center justify-between mt-3">
        <span className="text-xs text-slate-400">{formatDateTime(note.created_at)}</span>
        <button
          id={`delete-note-${note.id}`}
          onClick={() => onDelete(note.id)}
          disabled={deleting}
          className="text-xs text-red-500 hover:text-red-700 opacity-0 group-hover:opacity-100 transition-opacity disabled:opacity-50"
        >
          Delete
        </button>
      </div>
    </div>
  )
}
