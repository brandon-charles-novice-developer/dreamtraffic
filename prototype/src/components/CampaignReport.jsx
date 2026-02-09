import { campaign } from '../data/campaign'
import { dspStatuses } from '../data/dspStatus'
import { supplyPaths, dspComparison, lumaCpm, adspSavingsVsTtd } from '../data/supplyPaths'
import { measurementVendors } from '../data/vastXml'

export default function CampaignReport() {
  const approvedDsps = dspStatuses.filter(d => d.auditStatus === 'approved')
  const totalPaths = supplyPaths.length
  const adspPaths = supplyPaths.filter(p => p.dsp === 'Amazon DSP')
  const avgAdspNet = adspPaths.reduce((sum, p) => sum + (100 - p.dspFee - p.exchangeFee - p.sspFee), 0) / adspPaths.length
  const totalMeasurementCpm = measurementVendors.reduce((sum, v) => sum + v.cpm, 0)

  // Estimated impressions based on budget and $10 CPM
  const estimatedCpm = 10
  const estimatedImpressions = (campaign.budget / estimatedCpm) * 1000

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-white">Campaign Report</h2>
        <span className="text-xs text-slate-400">
          {new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}
        </span>
      </div>

      {/* Executive Summary */}
      <div className="bg-gradient-to-r from-blue-500/10 to-violet-500/10 rounded-xl p-6 border border-blue-500/20">
        <h3 className="text-sm font-semibold text-blue-200 mb-3">Executive Summary</h3>
        <p className="text-sm text-slate-300 leading-relaxed">
          <span className="font-semibold text-white">{campaign.name}</span> has completed the full DreamTraffic pipeline:
          AI-generated creative via Luma Dream Machine, compliance review, VAST 4.2 measurement wrapping,
          and multi-DSP trafficking across {dspStatuses.length} platforms. {approvedDsps.length} DSPs are audit-approved
          with {totalPaths} active supply paths mapped.
        </p>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard label="Campaign Budget" value={`$${(campaign.budget / 1000).toFixed(0)}K`} sub={`${campaign.flightStart} → ${campaign.flightEnd}`} />
        <MetricCard label="Est. Impressions" value={`${(estimatedImpressions / 1000000).toFixed(1)}M`} sub={`at $${estimatedCpm} CPM`} />
        <MetricCard label="DSPs Active" value={`${approvedDsps.length}/${dspStatuses.length}`} sub="audit approved" highlight />
        <MetricCard label="Supply Paths" value={totalPaths} sub="mapped routes" />
      </div>

      {/* Creative Summary */}
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <h3 className="text-sm font-semibold text-white mb-4">Creative Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-700/30">
            <div className="text-[10px] uppercase tracking-wider text-slate-500 mb-1">Generated</div>
            <div className="text-2xl font-bold text-white">1</div>
            <div className="text-xs text-slate-400 mt-1">Luma Dream Machine Ray2</div>
          </div>
          <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-700/30">
            <div className="text-[10px] uppercase tracking-wider text-slate-500 mb-1">Approved</div>
            <div className="text-2xl font-bold text-emerald-400">1</div>
            <div className="text-xs text-slate-400 mt-1">All compliance checks passed</div>
          </div>
          <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-700/30">
            <div className="text-[10px] uppercase tracking-wider text-slate-500 mb-1">Trafficked To</div>
            <div className="text-2xl font-bold text-blue-400">{dspStatuses.length}</div>
            <div className="text-xs text-slate-400 mt-1">DSP platforms</div>
          </div>
        </div>
      </div>

      {/* DSP Coverage */}
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <h3 className="text-sm font-semibold text-white mb-4">DSP Coverage</h3>
        <div className="space-y-3">
          {dspStatuses.map((dsp) => (
            <div key={dsp.key} className="flex items-center gap-3">
              <div className="w-3 h-3 rounded-full flex-shrink-0" style={{ backgroundColor: dsp.color }} />
              <span className="text-sm text-slate-200 w-32 flex-shrink-0">{dsp.dsp}</span>
              <div className="flex-1">
                <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all ${
                      dsp.auditStatus === 'approved' ? 'bg-emerald-500' : 'bg-amber-500'
                    }`}
                    style={{ width: dsp.auditStatus === 'approved' ? '100%' : '60%' }}
                  />
                </div>
              </div>
              <span className={`text-[10px] font-medium px-2 py-0.5 rounded border ${
                dsp.auditStatus === 'approved'
                  ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
                  : 'bg-amber-500/20 text-amber-400 border-amber-500/30'
              }`}>
                {dsp.auditStatus === 'approved' ? 'LIVE' : 'REVIEW'}
              </span>
              <span className="text-xs font-mono text-slate-400 w-10 text-right">{dsp.feeRate}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Impressions by Supply Path */}
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <h3 className="text-sm font-semibold text-white mb-4">Estimated Impressions by Supply Path</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr className="text-left text-[10px] uppercase tracking-wider text-slate-500">
                <th className="pb-2 pr-3">DSP</th>
                <th className="pb-2 pr-3">Exchange</th>
                <th className="pb-2 pr-3">SSP</th>
                <th className="pb-2 pr-3">Win Rate</th>
                <th className="pb-2 pr-3">Est. Impressions</th>
                <th className="pb-2">Pub Net</th>
              </tr>
            </thead>
            <tbody className="font-mono">
              {supplyPaths.map((p, i) => {
                const total = p.dspFee + p.exchangeFee + p.sspFee
                const net = 100 - total
                const pathImpressions = estimatedImpressions * p.winRate
                const isAdsp = p.dsp === 'Amazon DSP'
                return (
                  <tr key={i} className={`border-t border-slate-700/30 ${isAdsp ? 'bg-emerald-500/5' : ''}`}>
                    <td className="py-2 pr-3 text-slate-300">{p.dsp}</td>
                    <td className="py-2 pr-3 text-slate-400">{p.exchange}</td>
                    <td className="py-2 pr-3 text-slate-400">{p.ssp}</td>
                    <td className="py-2 pr-3 text-slate-300">{(p.winRate * 100).toFixed(0)}%</td>
                    <td className="py-2 pr-3 text-slate-200">{(pathImpressions / 1000000).toFixed(1)}M</td>
                    <td className={`py-2 font-medium ${isAdsp ? 'text-emerald-400' : 'text-slate-300'}`}>{net}%</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Fee Economics Summary */}
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <h3 className="text-sm font-semibold text-white mb-4">Fee Economics Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-emerald-500/5 rounded-lg p-4 border border-emerald-500/20">
            <div className="text-[10px] uppercase tracking-wider text-slate-500 mb-1">ADSP Advantage</div>
            <div className="text-2xl font-bold text-emerald-400">{adspSavingsVsTtd}%</div>
            <div className="text-xs text-slate-400 mt-1">lower supply cost vs. TTD</div>
          </div>
          <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-700/30">
            <div className="text-[10px] uppercase tracking-wider text-slate-500 mb-1">Luma Creative CPM</div>
            <div className="text-2xl font-bold text-white">${lumaCpm.toFixed(4)}</div>
            <div className="text-xs text-slate-400 mt-1">amortized generation cost</div>
          </div>
          <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-700/30">
            <div className="text-[10px] uppercase tracking-wider text-slate-500 mb-1">Measurement CPM</div>
            <div className="text-2xl font-bold text-white">${totalMeasurementCpm.toFixed(3)}</div>
            <div className="text-xs text-slate-400 mt-1">IAS + MOAT + DV combined</div>
          </div>
        </div>
        <div className="mt-4 bg-slate-900/50 rounded-lg p-4 border border-slate-700/30">
          <div className="flex items-center justify-between text-sm">
            <span className="text-slate-300">ADSP savings per 1K impressions vs. TTD</span>
            <span className="font-mono font-semibold text-emerald-400">${(estimatedCpm * adspSavingsVsTtd / 100).toFixed(2)}</span>
          </div>
          <div className="flex items-center justify-between text-sm mt-2">
            <span className="text-slate-300">Luma Dream Machine cost per 1K impressions</span>
            <span className="font-mono font-semibold text-white">${lumaCpm.toFixed(4)}</span>
          </div>
          <div className="border-t border-slate-700/50 mt-3 pt-3">
            <div className="flex items-center justify-between text-sm">
              <span className="text-emerald-300 font-medium">Net margin freed for AI creative</span>
              <span className="font-mono font-semibold text-emerald-400">
                ${((estimatedCpm * adspSavingsVsTtd / 100) - lumaCpm).toFixed(3)}/CPM
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Pipeline Status */}
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <h3 className="text-sm font-semibold text-white mb-4">Pipeline Completion</h3>
        <div className="space-y-3">
          {[
            { step: 'AI Creative Generation', detail: 'Luma Dream Machine Ray2', complete: true },
            { step: 'Compliance Review', detail: '8/8 checks passed', complete: true },
            { step: 'VAST 4.2 Wrapping', detail: 'IAS + MOAT + DV AdVerification', complete: true },
            { step: 'DSP Trafficking', detail: `${approvedDsps.length} approved, ${dspStatuses.length - approvedDsps.length} in review`, complete: true },
            { step: 'Supply Path Mapping', detail: `${totalPaths} paths across ${dspComparison.length} DSPs`, complete: true },
            { step: 'Fee Stack Analysis', detail: `ADSP optimal at ${avgAdspNet.toFixed(1)}% publisher net`, complete: true },
          ].map((item) => (
            <div key={item.step} className="flex items-center gap-3">
              <div className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] flex-shrink-0 ${
                item.complete
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
                  : 'bg-slate-700/50 text-slate-500 border border-slate-600/50'
              }`}>
                {item.complete ? '✓' : '○'}
              </div>
              <div className="flex-1">
                <span className="text-sm text-slate-200">{item.step}</span>
                <span className="text-xs text-slate-500 ml-2">{item.detail}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Footer Note */}
      <div className="bg-slate-800/30 rounded-lg p-3 border border-slate-700/30">
        <p className="text-[11px] text-slate-500">
          Report generated from DreamTraffic pipeline data. Impression estimates based on ${estimatedCpm} CPM
          across {totalPaths} supply paths. All DSP integrations use simulated API response shapes with realistic payloads.
          Backend source available on GitHub.
        </p>
      </div>
    </div>
  )
}

function MetricCard({ label, value, sub, highlight }) {
  return (
    <div className={`rounded-xl p-4 border ${
      highlight
        ? 'bg-emerald-500/5 border-emerald-500/20'
        : 'bg-slate-800/50 border-slate-700/50'
    }`}>
      <div className="text-[10px] uppercase tracking-wider text-slate-500">{label}</div>
      <div className={`text-2xl font-bold mt-1 ${highlight ? 'text-emerald-400' : 'text-white'}`}>{value}</div>
      <div className="text-xs text-slate-400 mt-1">{sub}</div>
    </div>
  )
}
