import { supplyPaths, dspComparison, lumaCpm, adspSavingsVsTtd } from '../data/supplyPaths'
import { dspStatuses } from '../data/dspStatus'

export default function SupplyChainMap() {
  const approvedDsps = dspStatuses.filter(d => d.auditStatus === 'approved')
  const reviewDsps = dspStatuses.filter(d => d.auditStatus !== 'approved')
  const openExchangePaths = supplyPaths.filter(p => p.dealType === 'Open Exchange')
  const pmpPaths = supplyPaths.filter(p => p.dealType === 'PMP')

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-white">Supply Chain Map</h2>
        <span className="text-xs text-slate-400">Social Video Repurposed for OLV Programmatic Activation</span>
      </div>

      {/* Step 1: DSP Readiness */}
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <div className="flex items-center gap-2 mb-4">
          <span className="text-xs font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30">STEP 1</span>
          <h3 className="text-sm font-semibold text-white">DSP Readiness — Creative Audit Status</h3>
        </div>
        <p className="text-xs text-slate-400 mb-4">
          Before activation, Dream Machine creative must pass each DSP's audit review. Once approved, the creative can serve via Open Exchange or PMP deals.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {dspStatuses.map((dsp) => {
            const isApproved = dsp.auditStatus === 'approved'
            return (
              <div key={dsp.key} className={`rounded-lg p-3 border ${isApproved ? 'bg-emerald-500/5 border-emerald-500/20' : 'bg-amber-500/5 border-amber-500/20'}`}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: dsp.color }} />
                    <span className="text-sm font-medium text-slate-200">{dsp.dsp}</span>
                  </div>
                  <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded border ${
                    isApproved
                      ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
                      : 'bg-amber-500/20 text-amber-400 border-amber-500/30'
                  }`}>
                    {isApproved ? 'READY' : 'IN REVIEW'}
                  </span>
                </div>
                <div className="text-[10px] text-slate-500 mt-1.5">
                  {dsp.feeRate} platform fee · {isApproved ? 'Open Exchange + PMP eligible' : 'Pending audit approval'}
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Step 2: Activation Paths — Visual Flow */}
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <div className="flex items-center gap-2 mb-4">
          <span className="text-xs font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30">STEP 2</span>
          <h3 className="text-sm font-semibold text-white">Activation Paths — DSP to Impression</h3>
        </div>
        <p className="text-xs text-slate-400 mb-5">
          Once approved, Dream Machine creative activates through multiple paths. Traffic directly in the DSP to reach Open Exchange inventory, route through Bidswitch or SmartSwitch to preferred SSPs, or execute PMP deals for premium guaranteed supply.
        </p>

        {/* Branching Flow Diagram */}
        <div className="space-y-6">
          {/* Source */}
          <div className="flex justify-center">
            <div className="flex flex-col items-center">
              <div className="w-24 h-14 rounded-2xl bg-gradient-to-br from-blue-500 to-violet-500 flex items-center justify-center shadow-lg">
                <span className="text-white text-[10px] font-bold text-center leading-tight">Luma AI<br/>Dream Machine</span>
              </div>
              <div className="w-px h-5 bg-slate-600 mt-1" />
              <span className="text-[9px] text-slate-500">VAST 4.2 wrapped creative</span>
              <div className="w-px h-4 bg-slate-600" />
            </div>
          </div>

          {/* DSP Tier */}
          <div className="bg-slate-900/50 rounded-xl p-4 border border-slate-700/30">
            <div className="text-[10px] uppercase tracking-wider text-slate-500 mb-3 text-center">Traffic in DSP</div>
            <div className="grid grid-cols-2 lg:grid-cols-5 gap-2">
              {dspStatuses.map((dsp) => {
                const isApproved = dsp.auditStatus === 'approved'
                return (
                  <div key={dsp.key} className="flex flex-col items-center">
                    <div className={`w-full h-10 rounded-lg flex items-center justify-center gap-1.5 border ${
                      isApproved ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-slate-700/30 border-slate-600/30'
                    }`}>
                      <div className="w-2 h-2 rounded-full" style={{ backgroundColor: dsp.color }} />
                      <span className={`text-[10px] font-medium ${isApproved ? 'text-emerald-300' : 'text-slate-500'}`}>{dsp.dsp}</span>
                    </div>
                    <span className="text-[9px] text-slate-600 mt-1">{dsp.feeRate}</span>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Branching: Exchange Routing + Deal Types */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            {/* Open Exchange Path */}
            <div className="bg-slate-900/50 rounded-xl p-4 border border-blue-500/20">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-6 h-6 rounded bg-blue-500/20 flex items-center justify-center text-[10px] text-blue-300">⇄</div>
                <div>
                  <div className="text-xs font-semibold text-blue-300">Open Exchange</div>
                  <div className="text-[10px] text-slate-500">Via Bidswitch</div>
                </div>
              </div>
              <div className="space-y-1.5">
                {['Magnite', 'PubMatic', 'Index Exchange'].map((ssp) => (
                  <div key={ssp} className="flex items-center justify-between py-1 px-2 rounded bg-slate-800/50">
                    <span className="text-[11px] text-slate-300">{ssp}</span>
                    <span className="text-[9px] text-blue-400">RTB</span>
                  </div>
                ))}
              </div>
            </div>

            {/* SmartSwitch Path */}
            <div className="bg-slate-900/50 rounded-xl p-4 border border-cyan-500/20">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-6 h-6 rounded bg-cyan-500/20 flex items-center justify-center text-[10px] text-cyan-300">⚡</div>
                <div>
                  <div className="text-xs font-semibold text-cyan-300">SmartSwitch</div>
                  <div className="text-[10px] text-slate-500">ML-optimized routing</div>
                </div>
              </div>
              <div className="space-y-1.5">
                {['Zeta Global', 'Magnite', 'PubMatic'].map((ssp) => (
                  <div key={ssp} className="flex items-center justify-between py-1 px-2 rounded bg-slate-800/50">
                    <span className="text-[11px] text-slate-300">{ssp}</span>
                    <span className="text-[9px] text-cyan-400">PMP</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Direct / PMP Path */}
            <div className="bg-slate-900/50 rounded-xl p-4 border border-emerald-500/20">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-6 h-6 rounded bg-emerald-500/20 flex items-center justify-center text-[10px] text-emerald-300">◎</div>
                <div>
                  <div className="text-xs font-semibold text-emerald-300">Direct / PMP Deal</div>
                  <div className="text-[10px] text-slate-500">No exchange fee</div>
                </div>
              </div>
              <div className="space-y-1.5">
                {['FreeWheel', 'Magnite PG', 'Index PG'].map((ssp) => (
                  <div key={ssp} className="flex items-center justify-between py-1 px-2 rounded bg-slate-800/50">
                    <span className="text-[11px] text-slate-300">{ssp}</span>
                    <span className="text-[9px] text-emerald-400">Guaranteed</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Impression Delivery */}
          <div className="flex justify-center">
            <div className="flex flex-col items-center">
              <div className="w-px h-4 bg-slate-600" />
              <div className="w-48 h-12 rounded-2xl bg-gradient-to-br from-pink-500 to-rose-500 flex items-center justify-center shadow-lg">
                <span className="text-white text-[10px] font-bold text-center leading-tight">Impression Served<br/>OLV Programmatic</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* DSP Comparison */}
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <h3 className="text-sm font-semibold text-white mb-4">DSP Fee Comparison — All Platforms</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-[11px] uppercase tracking-wider text-slate-500">
                <th className="pb-3 pr-4">DSP</th>
                <th className="pb-3 pr-4">Platform Fee</th>
                <th className="pb-3 pr-4">Total Supply Cost</th>
                <th className="pb-3 pr-4">Publisher Net</th>
                <th className="pb-3">Paths</th>
              </tr>
            </thead>
            <tbody>
              {dspComparison.map((row) => (
                <tr
                  key={row.dsp}
                  className={`border-t border-slate-700/30 ${row.highlight ? 'bg-emerald-500/5' : ''}`}
                >
                  <td className="py-3 pr-4">
                    <div className="flex items-center gap-2">
                      <span className={`text-sm font-medium ${row.highlight ? 'text-emerald-300' : 'text-slate-200'}`}>
                        {row.dsp}
                      </span>
                      {row.highlight && (
                        <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                          LOWEST
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="py-3 pr-4 font-mono text-slate-300">{row.avgDspFee}%</td>
                  <td className="py-3 pr-4 font-mono text-slate-300">{row.avgTotalCost}%</td>
                  <td className="py-3 pr-4 font-mono text-slate-300">{row.avgPublisherNet}%</td>
                  <td className="py-3 font-mono text-slate-400">{row.paths}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Fee Stack Breakdown */}
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <h3 className="text-sm font-semibold text-white mb-4">Fee Stack Analysis (on $10.00 CPM)</h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* ADSP Path */}
          <div className="bg-emerald-500/5 rounded-lg p-4 border border-emerald-500/20">
            <div className="text-xs font-semibold text-emerald-300 mb-3">Amazon DSP → Bidswitch → Magnite (Open Exchange)</div>
            <div className="space-y-2 font-mono text-xs">
              <FeeRow label="Luma Creative Gen" value={`$${lumaCpm.toFixed(4)}/CPM`} sub="amortized" />
              <FeeRow label="Amazon DSP Fee" value="12.0%" amount="$1.20" highlight />
              <FeeRow label="Bidswitch Exchange" value="2.0%" amount="$0.20" />
              <FeeRow label="Magnite SSP" value="15.0%" amount="$1.50" />
              <FeeRow label="IAS + MOAT + DV" value="$0.075/CPM" />
              <div className="border-t border-emerald-500/30 pt-2 mt-2">
                <FeeRow label="Total Supply Cost" value="29.0%" amount="$2.90" bold />
                <FeeRow label="Publisher Net" value="71.0%" amount="$7.10" bold />
              </div>
            </div>
          </div>

          {/* TTD Path */}
          <div className="bg-slate-700/30 rounded-lg p-4 border border-slate-600/30">
            <div className="text-xs font-semibold text-slate-300 mb-3">TTD → Bidswitch → Magnite (Open Exchange)</div>
            <div className="space-y-2 font-mono text-xs">
              <FeeRow label="Luma Creative Gen" value={`$${lumaCpm.toFixed(4)}/CPM`} sub="amortized" />
              <FeeRow label="TTD Platform Fee" value="15.0%" amount="$1.50" />
              <FeeRow label="Bidswitch Exchange" value="2.0%" amount="$0.20" />
              <FeeRow label="Magnite SSP" value="15.0%" amount="$1.50" />
              <FeeRow label="IAS + MOAT + DV" value="$0.075/CPM" />
              <div className="border-t border-slate-600/50 pt-2 mt-2">
                <FeeRow label="Total Supply Cost" value="32.0%" amount="$3.20" bold />
                <FeeRow label="Publisher Net" value="68.0%" amount="$6.80" bold />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Strategic Insight */}
      <div className="bg-gradient-to-r from-emerald-500/10 to-blue-500/10 rounded-xl p-6 border border-emerald-500/20">
        <h3 className="text-sm font-semibold text-emerald-300 mb-2">Strategic Insight</h3>
        <p className="text-sm text-slate-300 leading-relaxed">
          Amazon DSP's post-June 2025 fee reduction saves <span className="font-semibold text-emerald-300">{adspSavingsVsTtd}%</span> in
          supply cost vs. The Trade Desk. On a $10 CPM, that's <span className="font-semibold text-emerald-300">${(10 * adspSavingsVsTtd / 100).toFixed(2)}</span> per
          thousand impressions freed up — more than enough to cover Luma Dream Machine creative generation
          costs at <span className="font-mono text-emerald-300">${lumaCpm.toFixed(4)}/CPM</span>.
        </p>
        <p className="text-sm text-slate-400 mt-3">
          With {supplyPaths.length} activation paths across {dspComparison.length} DSPs — including Open Exchange, SmartSwitch, and Direct PMP deals —
          Luma captures value wherever the impression serves. ADSP's lower fees create the margin headroom;
          the breadth of SSP connectivity (Magnite, PubMatic, Index, Zeta, FreeWheel) ensures reach.
        </p>
      </div>

      {/* All Paths Table */}
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <h3 className="text-sm font-semibold text-white mb-4">All Supply Paths ({supplyPaths.length})</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr className="text-left text-[10px] uppercase tracking-wider text-slate-500">
                <th className="pb-2 pr-3">DSP</th>
                <th className="pb-2 pr-3">Exchange</th>
                <th className="pb-2 pr-3">SSP</th>
                <th className="pb-2 pr-3">Deal Type</th>
                <th className="pb-2 pr-3">DSP Fee</th>
                <th className="pb-2 pr-3">Exch Fee</th>
                <th className="pb-2 pr-3">SSP Fee</th>
                <th className="pb-2 pr-3">Total</th>
                <th className="pb-2">Pub Net</th>
              </tr>
            </thead>
            <tbody className="font-mono">
              {supplyPaths.map((p, i) => {
                const total = p.dspFee + p.exchangeFee + p.sspFee
                const net = 100 - total
                const isAdsp = p.dsp === 'Amazon DSP'
                return (
                  <tr key={i} className={`border-t border-slate-700/30 ${isAdsp ? 'bg-emerald-500/5' : ''}`}>
                    <td className="py-2 pr-3 text-slate-300">{p.dsp}</td>
                    <td className="py-2 pr-3 text-slate-400">{p.exchange}</td>
                    <td className="py-2 pr-3 text-slate-400">{p.ssp}</td>
                    <td className="py-2 pr-3">
                      <span className={`text-[9px] font-medium px-1.5 py-0.5 rounded border ${
                        p.dealType === 'PMP'
                          ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                          : 'bg-blue-500/10 text-blue-400 border-blue-500/20'
                      }`}>
                        {p.dealType}
                      </span>
                    </td>
                    <td className="py-2 pr-3 text-slate-300">{p.dspFee}%</td>
                    <td className="py-2 pr-3 text-slate-400">{p.exchangeFee}%</td>
                    <td className="py-2 pr-3 text-slate-400">{p.sspFee}%</td>
                    <td className="py-2 pr-3 text-slate-200">{total}%</td>
                    <td className={`py-2 font-medium ${isAdsp ? 'text-emerald-400' : 'text-slate-300'}`}>{net}%</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

function FeeRow({ label, value, amount, sub, highlight, bold }) {
  return (
    <div className={`flex items-center justify-between ${bold ? 'font-semibold' : ''}`}>
      <span className={`${highlight ? 'text-emerald-300' : 'text-slate-400'}`}>
        {label}
        {sub && <span className="text-slate-600 ml-1">({sub})</span>}
      </span>
      <div className="flex items-center gap-3">
        <span className="text-slate-300">{value}</span>
        {amount && <span className="text-slate-500 w-12 text-right">{amount}</span>}
      </div>
    </div>
  )
}
