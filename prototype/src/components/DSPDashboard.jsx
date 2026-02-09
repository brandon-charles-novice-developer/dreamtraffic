import { dspStatuses } from '../data/dspStatus'

const auditColors = {
  approved: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
  under_review: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
  pending: 'bg-slate-500/20 text-slate-400 border-slate-500/30',
  rejected: 'bg-red-500/20 text-red-400 border-red-500/30',
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
        <h2 className="text-xl font-semibold text-white">DSP Trafficking Dashboard</h2>
        <span className="text-xs text-slate-400">
          {approvedCount}/{dspStatuses.length} DSPs Approved
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {dspStatuses.map((dsp) => (
          <div
            key={dsp.key}
            className="bg-slate-800/50 rounded-xl border border-slate-700/50 overflow-hidden"
          >
            {/* Header with DSP color accent */}
            <div className="px-5 py-3 border-b border-slate-700/50 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: dsp.color }}
                />
                <span className="text-sm font-semibold text-white">{dsp.dsp}</span>
              </div>
              <span className={`inline-flex px-2 py-0.5 rounded text-[10px] font-medium border ${auditColors[dsp.auditStatus]}`}>
                {auditLabels[dsp.auditStatus]}
              </span>
            </div>

            <div className="p-5 space-y-3">
              {/* IDs */}
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <div className="text-[10px] uppercase tracking-wider text-slate-500">Creative ID</div>
                  <div className="text-[11px] font-mono text-slate-300 mt-0.5 truncate">{dsp.creativeId}</div>
                </div>
                <div>
                  <div className="text-[10px] uppercase tracking-wider text-slate-500">Platform Fee</div>
                  <div className="text-sm font-medium text-slate-200 mt-0.5">{dsp.feeRate}</div>
                </div>
              </div>

              {/* Features */}
              <div>
                <div className="text-[10px] uppercase tracking-wider text-slate-500 mb-1.5">Capabilities</div>
                <div className="space-y-1">
                  {dsp.features.map((f, i) => (
                    <div key={i} className="flex items-start gap-1.5">
                      <span className="text-slate-600 text-xs mt-0.5">·</span>
                      <span className="text-[11px] text-slate-400">{f}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Certified Supply (Amazon only) */}
              {dsp.certifiedSupply.length > 0 && (
                <div>
                  <div className="text-[10px] uppercase tracking-wider text-slate-500 mb-1.5">
                    Certified Supply Exchange
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {dsp.certifiedSupply.map((s) => (
                      <span
                        key={s}
                        className="px-2 py-0.5 rounded text-[10px] bg-amber-500/10 text-amber-300 border border-amber-500/20"
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
                      <div className={`h-1 flex-1 rounded-full ${isComplete ? 'bg-emerald-500/50' : 'bg-slate-700/50'}`} />
                    </div>
                  )
                })}
              </div>
              <div className="flex justify-between mt-1">
                <span className="text-[9px] text-slate-500">Upload</span>
                <span className="text-[9px] text-slate-500">Audit</span>
                <span className="text-[9px] text-slate-500">Active</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Simulated Notice */}
      <div className="bg-slate-800/30 rounded-lg p-3 border border-slate-700/30">
        <p className="text-[11px] text-slate-500">
          DSP integrations are simulated with realistic API response shapes. The backend includes full request/response payloads for each platform.
          Amazon DSP adapter mirrors the MCP Server pattern launched February 2, 2026.
        </p>
      </div>
    </div>
  )
}
