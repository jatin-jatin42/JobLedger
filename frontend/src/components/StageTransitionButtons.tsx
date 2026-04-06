import { VALID_TRANSITIONS, STAGE_CONFIG, Stage } from '../utils/stageConfig'

interface StageTransitionButtonsProps {
  currentStage: string
  onTransition: (stage: Stage) => void
  loading?: boolean
}

export default function StageTransitionButtons({
  currentStage,
  onTransition,
  loading = false,
}: StageTransitionButtonsProps) {
  const validNext = VALID_TRANSITIONS[currentStage as Stage] ?? []

  if (validNext.length === 0) {
    return (
      <p className="text-sm text-slate-400 italic">
        This application is in a terminal stage — no further transitions.
      </p>
    )
  }

  return (
    <div className="flex flex-wrap gap-2">
      {validNext.map((stage) => {
        const config = STAGE_CONFIG[stage]
        const isDestructive = stage === 'REJECTED' || stage === 'WITHDRAWN'
        return (
          <button
            key={stage}
            id={`transition-btn-${stage.toLowerCase()}`}
            onClick={() => onTransition(stage)}
            disabled={loading}
            className={`btn text-xs px-3 py-1.5 ring-1 ${config.color} ${config.bg} ${config.ring} hover:opacity-80 ${isDestructive ? 'opacity-70' : ''}`}
          >
            → {config.label}
          </button>
        )
      })}
    </div>
  )
}
