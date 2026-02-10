import { dspStatuses } from '../data/dspStatus'

const auditColors = {
  approved: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  under_review: 'bg-amber-50 text-amber-700 border-amber-200',
  pending: 'bg-neutral-100 text-neutral-500 border-neutral-200',
  rejected: 'bg-red-50 text-red-700 border-red-200',
}

const auditLabels = {
  approved: 'Approved',
  under_review: 'Under Review',
  pending: 'Pending',
  rejected: 'Rejected',
}

export default function DSPDashboard() {
  const approvedCount = dspStatuses.filter(d => d.auditStatus === 'approved').length

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-neutral-900">DSP Trafficking Dashboard</h2>
        <span className="text-xs text-neutral-500">
          {approvedCount}/{dspStatuses.length} DSPs Approved
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {dspStatuses.map((dsp) => (
          <div
            key={dsp.key}
            className="bg-white rounded-2xl border border-neutral-200 overflow-hidden"
          >
            {/* Header */}
            <div className="px-5 py-3 border-b border-neutral-100 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: dsp.color }}
                />
                <span className="text-sm font-semibold text-neutral-900">{dsp.dsp}</span>
              </div>
              <span className={`inline-flex px-2 py-0.5 rounded text-[10px] font-medium border ${auditColors[dsp.auditStatus]}`}>
                {auditLabels[dsp.auditStatus]}
              </span>
            </div>

            <div className="p-5 space-y-3">
              {/* IDs */}
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <div className="text-[10px] uppercase tracking-wider text-neutral-400">Creative ID</div>
                  <div className="text-[11px] font-mono text-neutral-600 mt-0.5 truncate">{dsp.creativeId}</div>
                </div>
                <div>
                  <div className="text-[10px] uppercase tracking-wider text-neutral-400">Platform Fee</div>
                  <div className="text-sm font-semibold text-neutral-900 mt-0.5">{dsp.feeRate}</div>
                </div>
              </div>

              {/* Features */}
              <div>
                <div className="text-[10px] uppercase tracking-wider text-neutral-400 mb-1.5">Capabilities</div>
                <div className="space-y-1">
                  {dsp.features.map((f, i) => (
                    <div key={i} className="flex items-start gap-1.5">
                      <span className="text-neutral-300 text-xs mt-0.5">·</span>
                      <span className="text-[11px] text-neutral-600">{f}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Certified Supply */}
              {dsp.certifiedSupply.length > 0 && (
                <div>
                  <div className="text-[10px] uppercase tracking-wider text-neutral-400 mb-1.5">
                    Certified Supply Exchange
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {dsp.certifiedSupply.map((s) => (
                      <span
                        key={s}
                        className="px-2 py-0.5 rounded text-[10px] bg-neutral-100 text-neutral-700 border border-neutral-200"
                      >
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Audit Progress Bar */}
            <div className="px-5 pb-4">
              <div className="flex items-center gap-2">
                {['Upload', 'Audit', 'Active'].map((step, i) => {
                  const isComplete = dsp.auditStatus === 'approved'
                    ? true
                    : dsp.auditStatus === 'under_review'
                      ? i < 2
                      : i < 1
                  return (
                    <div key={step} className="flex items-center gap-2 flex-1">
                      <div className={`h-1.5 flex-1 rounded-full ${isComplete ? 'bg-neutral-900' : 'bg-neutral-200'}`} />
                    </div>
                  )
                })}
              </div>
              <div className="flex justify-between mt-1">
                <span className="text-[9px] text-neutral-400">Upload</span>
                <span className="text-[9px] text-neutral-400">Audit</span>
                <span className="text-[9px] text-neutral-400">Active</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-neutral-50 rounded-2xl p-3 border border-neutral-200">
        <p className="text-[11px] text-neutral-400">
          DSP integrations are simulated with realistic API response shapes. The backend includes full request/response payloads for each platform.
          Amazon DSP adapter mirrors the MCP Server pattern launched February 2, 2026.
        </p>
      </div>
    </div>
  )
}
