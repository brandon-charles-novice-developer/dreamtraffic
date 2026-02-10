import { approvalTimeline, complianceChecks } from '../data/approvalTimeline'

const statusColors = {
  draft: 'bg-neutral-100 text-neutral-500 border-neutral-200',
  pending_review: 'bg-amber-50 text-amber-700 border-amber-200',
  approved: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  trafficked: 'bg-blue-50 text-blue-700 border-blue-200',
  active: 'bg-neutral-900 text-white border-neutral-900',
}

const statusLabels = {
  draft: 'Draft',
  pending_review: 'Pending Review',
  approved: 'Approved',
  trafficked: 'Trafficked',
  active: 'Active',
}

export default function ApprovalWorkflow() {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-neutral-900">Approval Workflow</h2>

      {/* Status Timeline */}
      <div className="bg-white rounded-2xl p-6 border border-neutral-200">
        <h3 className="text-sm font-semibold text-neutral-900 mb-5">Status Timeline</h3>
        <div className="flex items-center gap-3 mb-6 flex-wrap">
          {['draft', 'pending_review', 'approved', 'trafficked', 'active'].map((status, i, arr) => (
            <div key={status} className="flex items-center gap-3">
              <span className={`inline-flex px-2.5 py-1 rounded-lg text-[11px] font-medium border ${statusColors[status]}`}>
                {statusLabels[status]}
              </span>
              {i < arr.length - 1 && (
                <span className="text-neutral-300">→</span>
              )}
            </div>
          ))}
        </div>

        {/* Events */}
        <div className="space-y-0 relative">
          <div className="absolute left-[11px] top-3 bottom-3 w-px bg-neutral-200" />
          {approvalTimeline.map((event, i) => (
            <div key={i} className="flex gap-4 relative pb-6 last:pb-0">
              <div className="w-6 h-6 rounded-full bg-neutral-900 flex items-center justify-center text-white text-[10px] flex-shrink-0 z-10">
                ✓
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className={`inline-flex px-2 py-0.5 rounded text-[10px] font-medium border ${statusColors[event.fromStatus]}`}>
                    {statusLabels[event.fromStatus]}
                  </span>
                  <span className="text-neutral-300 text-xs">→</span>
                  <span className={`inline-flex px-2 py-0.5 rounded text-[10px] font-medium border ${statusColors[event.toStatus]}`}>
                    {statusLabels[event.toStatus]}
                  </span>
                  <span className="text-neutral-400 text-[10px] ml-auto">
                    {new Date(event.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
                <div className="text-xs text-neutral-500 mt-1">
                  <span className="text-neutral-700 font-medium">{event.reviewer}</span>
                  {' — '}{event.notes}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Compliance Checks */}
      <div className="bg-white rounded-2xl p-6 border border-neutral-200">
        <h3 className="text-sm font-semibold text-neutral-900 mb-4">Compliance Validation</h3>
        <div className="space-y-2">
          {complianceChecks.map((check) => (
            <div
              key={check.check}
              className="flex items-start gap-3 py-2 border-b border-neutral-100 last:border-0"
            >
              <span className={`mt-0.5 text-xs font-bold px-1.5 py-0.5 rounded ${
                check.status === 'pass'
                  ? 'bg-emerald-50 text-emerald-700'
                  : 'bg-red-50 text-red-700'
              }`}>
                {check.status === 'pass' ? 'PASS' : 'FAIL'}
              </span>
              <div className="flex-1 min-w-0">
                <div className="text-sm text-neutral-800">{check.check}</div>
                <div className="text-xs text-neutral-500 mt-0.5">{check.detail}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
