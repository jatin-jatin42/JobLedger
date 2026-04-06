import { STAGE_CONFIG, Stage } from '../utils/stageConfig'

interface StageBadgeProps {
  stage: string
  size?: 'sm' | 'md'
}

export default function StageBadge({ stage, size = 'md' }: StageBadgeProps) {
  const config = STAGE_CONFIG[stage as Stage]
  if (!config) return <span className="text-slate-400 text-xs">Unknown</span>

  const sizeClass = size === 'sm' ? 'text-xs px-2 py-0.5' : 'text-xs px-2.5 py-1'

  return (
    <span
      className={`inline-flex items-center font-medium rounded-full ring-1 ${sizeClass} ${config.color} ${config.bg} ${config.ring}`}
    >
      {config.label}
    </span>
  )
}
