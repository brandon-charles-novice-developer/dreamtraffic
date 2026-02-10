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
  const estimatedCpm = 10
  const estimatedImpressions = (campaign.budget / estimatedCpm) * 1000

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-neutral-900">Campaign Report</h2>
        <span className="text-xs text-neutral-500">
          {new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}
        </span>
      </div>

      <div className="bg-neutral-900 rounded-2xl p-6 text-white">
        <h3 className="text-sm font-semibold mb-3">Executive Summary</h3>
        <p className="text-sm text-neutral-300 leading-relaxed">
          <span className="font-semibold text-white">{campaign.name}</span> has completed the full pipeline:
          AI-generated creative via Luma Dream Machine, compliance review, VAST 4.2 measurement wrapping,
          and multi-DSP trafficking across {dspStatuses.length} platforms. {approvedDsps.length} DSPs are audit-approved
          with {totalPaths} active supply paths mapped.
        </p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard label="Campaign Budget" value={`$${(campaign.budget / 1000).toFixed(0)}K`} sub={`${campaign.flightStart} → ${campaign.flightEnd}`} />
        <MetricCard label="Est. Impressions" value={`${(estimatedImpressions / 1000000).toFixed(1)}M`} sub={`at $${estimatedCpm} CPM`} />
        <MetricCard label="DSPs Active" value={`${approvedDsps.length}/${dspStatuses.length}`} sub="audit approved" highlight />
        <MetricCard label="Supply Paths" value={totalPaths} sub="mapped routes" />
      </div>

      <div className="bg-white rounded-2xl p-6 border border-neutral-200">
        <h3 className="text-sm font-semibold text-neutral-900 mb-4">Creative Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-neutral-50 rounded-xl p-4 border border-neutral-200">
            <div className="text-[10px] uppercase tracking-wider text-neutral-400 mb-1">Generated</div>
            <div className="text-2xl font-bold text-neutral-900">1</div>
            <div className="text-xs text-neutral-500 mt-1">Luma Dream Machine Ray2</div>
          </div>
          <div className="bg-neutral-50 rounded-xl p-4 border border-neutral-200">
            <div className="text-[10px] uppercase tracking-wider text-neutral-400 mb-1">Approved</div>
            <div className="text-2xl font-bold text-emerald-700">1</div>
            <div className="text-xs text-neutral-500 mt-1">All compliance checks passed</div>
          </div>
          <div className="bg-neutral-50 rounded-xl p-4 border border-neutral-200">
            <div className="text-[10px] uppercase tracking-wider text-neutral-400 mb-1">Trafficked To</div>
            <div className="text-2xl font-bold text-neutral-900">{dspStatuses.length}</div>
            <div className="text-xs text-neutral-500 mt-1">DSP platforms</div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl p-6 border border-neutral-200">
        <h3 className="text-sm font-semibold text-neutral-900 mb-4">DSP Coverage</h3>
        <div className="space-y-3">
          {dspStatuses.map((dsp) => (
            <div key={dsp.key} className="flex items-center gap-3">
              <div className="w-3 h-3 rounded-full flex-shrink-0" style={{ backgroundColor: dsp.color }} />
              <span className="text-sm text-neutral-800 w-32 flex-shrink-0">{dsp.dsp}</span>
              <div className="flex-1">
                <div className="h-2 bg-neutral-100 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all ${dsp.auditStatus === 'approved' ? 'bg-neutral-900' : 'bg-amber-400'}`}
                    style={{ width: dsp.auditStatus === 'approved' ? '100%' : '60%' }}
                  />
                </div>
              </div>
              <span className={`text-[10px] font-medium px-2 py-0.5 rounded ${
                dsp.auditStatus === 'approved' ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'
              }`}>
                {dsp.auditStatus === 'approved' ? 'LIVE' : 'REVIEW'}
              </span>
              <span className="text-xs font-mono text-neutral-500 w-10 text-right">{dsp.feeRate}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-2xl p-6 border border-neutral-200">
        <h3 className="text-sm font-semibold text-neutral-900 mb-4">Fee Economics Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-emerald-50 rounded-xl p-4 border border-emerald-200">
            <div className="text-[10px] uppercase tracking-wider text-neutral-400 mb-1">ADSP Advantage</div>
            <div className="text-2xl font-bold text-emerald-700">{adspSavingsVsTtd}%</div>
            <div className="text-xs text-neutral-500 mt-1">lower supply cost vs. TTD</div>
          </div>
          <div className="bg-neutral-50 rounded-xl p-4 border border-neutral-200">
            <div className="text-[10px] uppercase tracking-wider text-neutral-400 mb-1">Luma Creative CPM</div>
            <div className="text-2xl font-bold text-neutral-900">${lumaCpm.toFixed(4)}</div>
            <div className="text-xs text-neutral-500 mt-1">amortized generation cost</div>
          </div>
          <div className="bg-neutral-50 rounded-xl p-4 border border-neutral-200">
            <div className="text-[10px] uppercase tracking-wider text-neutral-400 mb-1">Measurement CPM</div>
            <div className="text-2xl font-bold text-neutral-900">${totalMeasurementCpm.toFixed(3)}</div>
            <div className="text-xs text-neutral-500 mt-1">IAS + MOAT + DV combined</div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl p-6 border border-neutral-200">
        <h3 className="text-sm font-semibold text-neutral-900 mb-4">Pipeline Completion</h3>
        <div className="space-y-3">
          {[
            { step: 'AI Creative Generation', detail: 'Luma Dream Machine Ray2' },
            { step: 'Compliance Review', detail: '8/8 checks passed' },
            { step: 'VAST 4.2 Wrapping', detail: 'IAS + MOAT + DV AdVerification' },
            { step: 'DSP Trafficking', detail: `${approvedDsps.length} approved, ${dspStatuses.length - approvedDsps.length} in review` },
            { step: 'Supply Path Mapping', detail: `${totalPaths} paths across ${dspComparison.length} DSPs` },
            { step: 'Fee Stack Analysis', detail: `ADSP optimal at ${avgAdspNet.toFixed(1)}% publisher net` },
          ].map((item) => (
            <div key={item.step} className="flex items-center gap-3">
              <div className="w-5 h-5 rounded-full bg-neutral-900 flex items-center justify-center text-[10px] text-white flex-shrink-0">
                ✓
              </div>
              <div className="flex-1">
                <span className="text-sm text-neutral-800">{item.step}</span>
                <span className="text-xs text-neutral-400 ml-2">{item.detail}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-neutral-50 rounded-2xl p-3 border border-neutral-200">
        <p className="text-[11px] text-neutral-400">
          Report generated from Luma Dream Traffic Machine pipeline data. Impression estimates based on ${estimatedCpm} CPM
          across {totalPaths} supply paths. All DSP integrations use simulated API response shapes with realistic payloads.
        </p>
      </div>
    </div>
  )
}

function MetricCard({ label, value, sub, highlight }) {
  return (
    <div className={`rounded-2xl p-4 border ${highlight ? 'bg-emerald-50 border-emerald-200' : 'bg-white border-neutral-200'}`}>
      <div className="text-[10px] uppercase tracking-wider text-neutral-400">{label}</div>
      <div className={`text-2xl font-bold mt-1 ${highlight ? 'text-emerald-700' : 'text-neutral-900'}`}>{value}</div>
      <div className="text-xs text-neutral-500 mt-1">{sub}</div>
    </div>
  )
}
