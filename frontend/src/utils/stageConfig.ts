export type Stage = 'APPLIED' | 'SCREENING' | 'INTERVIEW' | 'OFFER' | 'REJECTED' | 'WITHDRAWN'

export interface StageConfig {
  label: string
  color: string        // Tailwind text color
  bg: string          // Tailwind bg color
  ring: string        // Tailwind ring color
  hex: string         // Hex for inline styles
}

// Mirrors VALID_TRANSITIONS in backend/app/services/application_service.py
// Frontend uses this for UI hints only — backend enforces the actual rules
export const VALID_TRANSITIONS: Record<Stage, Stage[]> = {
  APPLIED:   ['SCREENING', 'REJECTED', 'WITHDRAWN'],
  SCREENING: ['INTERVIEW', 'REJECTED', 'WITHDRAWN'],
  INTERVIEW: ['OFFER',     'REJECTED', 'WITHDRAWN'],
  OFFER:     ['REJECTED',  'WITHDRAWN'],
  REJECTED:  [],
  WITHDRAWN: [],
}

export const STAGE_CONFIG: Record<Stage, StageConfig> = {
  APPLIED: {
    label: 'Applied',
    color: 'text-blue-700',
    bg: 'bg-blue-100',
    ring: 'ring-blue-200',
    hex: '#3B82F6',
  },
  SCREENING: {
    label: 'Screening',
    color: 'text-amber-700',
    bg: 'bg-amber-100',
    ring: 'ring-amber-200',
    hex: '#F59E0B',
  },
  INTERVIEW: {
    label: 'Interview',
    color: 'text-violet-700',
    bg: 'bg-violet-100',
    ring: 'ring-violet-200',
    hex: '#8B5CF6',
  },
  OFFER: {
    label: 'Offer',
    color: 'text-green-700',
    bg: 'bg-green-100',
    ring: 'ring-green-200',
    hex: '#22C55E',
  },
  REJECTED: {
    label: 'Rejected',
    color: 'text-red-700',
    bg: 'bg-red-100',
    ring: 'ring-red-200',
    hex: '#EF4444',
  },
  WITHDRAWN: {
    label: 'Withdrawn',
    color: 'text-slate-600',
    bg: 'bg-slate-100',
    ring: 'ring-slate-200',
    hex: '#6B7280',
  },
}

export const ALL_STAGES: Stage[] = ['APPLIED', 'SCREENING', 'INTERVIEW', 'OFFER', 'REJECTED', 'WITHDRAWN']
