import { supplyPaths, dspComparison, lumaCpm, adspSavingsVsTtd } from '../data/supplyPaths'
import { dspStatuses } from '../data/dspStatus'

export default function SupplyChainMap() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-neutral-900">Supply Chain Map</h2>
        <span className="text-xs text-neutral-500">Social Video Repurposed for OLV Programmatic Activation</span>
      </div>

      {/* Step 1: DSP Readiness */}
      <div className="bg-white rounded-2xl p-6 border border-neutral-200">
        <div className="flex items-center gap-2 mb-4">
          <span className="text-xs font-bold px-2 py-0.5 rounded bg-neutral-900 text-white">STEP 1</span>
          <h3 className="text-sm font-semibold text-neutral-900">DSP Readiness — Creative Audit Status</h3>
        </div>
        <p className="text-xs text-neutral-500 mb-4">
          Before activation, Dream Machine creative must pass each DSP's audit review. Once approved, the creative can serve via Open Exchange or PMP deals.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {dspStatuses.map((dsp) => {
            const isApproved = dsp.auditStatus === 'approved'
            return (
              <div key={dsp.key} className={`rounded-xl p-3 border ${isApproved ? 'bg-emerald-50 border-emerald-200' : 'bg-amber-50 border-amber-200'}`}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: dsp.color }} />
                    <span className="text-sm font-medium text-neutral-800">{dsp.dsp}</span>
                  </div>
                  <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded ${
                    isApproved ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'
                  }`}>
                    {isApproved ? 'READY' : 'IN REVIEW'}
                  </span>
                </div>
                <div className="text-[10px] text-neutral-500 mt-1.5">
                  {dsp.feeRate} platform fee · {isApproved ? 'Open Exchange + PMP eligible' : 'Pending audit approval'}
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Step 2: Activation Paths */}
      <div className="bg-white rounded-2xl p-6 border border-neutral-200">
        <div className="flex items-center gap-2 mb-4">
          <span className="text-xs font-bold px-2 py-0.5 rounded bg-neutral-900 text-white">STEP 2</span>
          <h3 className="text-sm font-semibold text-neutral-900">Activation Paths — DSP to Impression</h3>
        </div>
        <p className="text-xs text-neutral-500 mb-5">
          Once approved, Dream Machine creative activates through multiple paths. Traffic directly in the DSP to reach Open Exchange inventory, route through Bidswitch or SmartSwitch to preferred SSPs, or execute PMP deals for premium guaranteed supply.
        </p>

        <div className="space-y-6">
          <div className="flex justify-center">
            <div className="flex flex-col items-center">
              <div className="w-24 h-14 rounded-2xl bg-neutral-900 flex items-center justify-center shadow-sm">
                <span className="text-white text-[10px] font-bold text-center leading-tight">Luma AI<br/>Dream Machine</span>
              </div>
              <div className="w-px h-5 bg-neutral-300 mt-1" />
              <span className="text-[9px] text-neutral-400">VAST 4.2 wrapped creative</span>
              <div className="w-px h-4 bg-neutral-300" />
            </div>
          </div>

          <div className="bg-neutral-50 rounded-xl p-4 border border-neutral-200">
            <div className="text-[10px] uppercase tracking-wider text-neutral-400 mb-3 text-center">Traffic in DSP</div>
            <div className="grid grid-cols-2 lg:grid-cols-5 gap-2">
              {dspStatuses.map((dsp) => {
                const isApproved = dsp.auditStatus === 'approved'
                return (
                  <div key={dsp.key} className="flex flex-col items-center">
                    <div className={`w-full h-10 rounded-lg flex items-center justify-center gap-1.5 border ${
                      isApproved ? 'bg-white border-neutral-300' : 'bg-neutral-100 border-neutral-200'
                    }`}>
                      <div className="w-2 h-2 rounded-full" style={{ backgroundColor: dsp.color }} />
                      <span className={`text-[10px] font-medium ${isApproved ? 'text-neutral-800' : 'text-neutral-400'}`}>{dsp.dsp}</span>
                    </div>
                    <span className="text-[9px] text-neutral-400 mt-1">{dsp.feeRate}</span>
                  </div>
                )
              })}
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <div className="bg-neutral-50 rounded-xl p-4 border border-blue-200">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-6 h-6 rounded bg-blue-100 flex items-center justify-center text-[10px] text-blue-700">⇄</div>
                <div>
                  <div className="text-xs font-semibold text-blue-800">Open Exchange</div>
                  <div className="text-[10px] text-neutral-500">Via Bidswitch</div>
                </div>
              </div>
              <div className="space-y-1.5">
                {['Magnite', 'PubMatic', 'Index Exchange'].map((ssp) => (
                  <div key={ssp} className="flex items-center justify-between py-1 px-2 rounded bg-white border border-neutral-200">
                    <span className="text-[11px] text-neutral-700">{ssp}</span>
                    <span className="text-[9px] font-medium text-blue-600">RTB</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-neutral-50 rounded-xl p-4 border border-violet-200">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-6 h-6 rounded bg-violet-100 flex items-center justify-center text-[10px] text-violet-700">⚡</div>
                <div>
                  <div className="text-xs font-semibold text-violet-800">SmartSwitch</div>
                  <div className="text-[10px] text-neutral-500">ML-optimized routing</div>
                </div>
              </div>
              <div className="space-y-1.5">
                {['Zeta Global', 'Magnite', 'PubMatic'].map((ssp) => (
                  <div key={ssp} className="flex items-center justify-between py-1 px-2 rounded bg-white border border-neutral-200">
                    <span className="text-[11px] text-neutral-700">{ssp}</span>
                    <span className="text-[9px] font-medium text-violet-600">PMP</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-neutral-50 rounded-xl p-4 border border-emerald-200">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-6 h-6 rounded bg-emerald-100 flex items-center justify-center text-[10px] text-emerald-700">◎</div>
                <div>
                  <div className="text-xs font-semibold text-emerald-800">Direct / PMP Deal</div>
                  <div className="text-[10px] text-neutral-500">No exchange fee</div>
                </div>
              </div>
              <div className="space-y-1.5">
                {['FreeWheel', 'Magnite PG', 'Index PG'].map((ssp) => (
                  <div key={ssp} className="flex items-center justify-between py-1 px-2 rounded bg-white border border-neutral-200">
                    <span className="text-[11px] text-neutral-700">{ssp}</span>
                    <span className="text-[9px] font-medium text-emerald-600">Guaranteed</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="flex justify-center">
            <div className="flex flex-col items-center">
              <div className="w-px h-4 bg-neutral-300" />
              <div className="w-48 h-12 rounded-2xl bg-neutral-900 flex items-center justify-center shadow-sm">
                <span className="text-white text-[10px] font-bold text-center leading-tight">Impression Served<br/>OLV Programmatic</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* DSP Comparison */}
      <div className="bg-white rounded-2xl p-6 border border-neutral-200">
        <h3 className="text-sm font-semibold text-neutral-900 mb-4">DSP Fee Comparison — All Platforms</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-[11px] uppercase tracking-wider text-neutral-400">
                <th className="pb-3 pr-4">DSP</th>
                <th className="pb-3 pr-4">Platform Fee</th>
                <th className="pb-3 pr-4">Total Supply Cost</th>
                <th className="pb-3 pr-4">Publisher Net</th>
                <th className="pb-3">Paths</th>
              </tr>
            </thead>
            <tbody>
              {dspComparison.map((row) => (
                <tr key={row.dsp} className={`border-t border-neutral-100 ${row.highlight ? 'bg-emerald-50' : ''}`}>
                  <td className="py-3 pr-4">
                    <div className="flex items-center gap-2">
                      <span className={`text-sm font-medium ${row.highlight ? 'text-emerald-800' : 'text-neutral-800'}`}>{row.dsp}</span>
                      {row.highlight && (
                        <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-emerald-100 text-emerald-700">LOWEST</span>
                      )}
                    </div>
                  </td>
                  <td className="py-3 pr-4 font-mono text-neutral-700">{row.avgDspFee}%</td>
                  <td className="py-3 pr-4 font-mono text-neutral-700">{row.avgTotalCost}%</td>
                  <td className="py-3 pr-4 font-mono text-neutral-700">{row.avgPublisherNet}%</td>
                  <td className="py-3 font-mono text-neutral-500">{row.paths}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Fee Stack */}
      <div className="bg-white rounded-2xl p-6 border border-neutral-200">
        <h3 className="text-sm font-semibold text-neutral-900 mb-4">Fee Stack Analysis (on $10.00 CPM)</h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-emerald-50 rounded-xl p-4 border border-emerald-200">
            <div className="text-xs font-semibold text-emerald-800 mb-3">Amazon DSP → Bidswitch → Magnite (Open Exchange)</div>
            <div className="space-y-2 font-mono text-xs">
              <FeeRow label="Luma Creative Gen" value={`$${lumaCpm.toFixed(4)}/CPM`} sub="amortized" />
              <FeeRow label="Amazon DSP Fee" value="12.0%" amount="$1.20" highlight />
              <FeeRow label="Bidswitch Exchange" value="2.0%" amount="$0.20" />
              <FeeRow label="Magnite SSP" value="15.0%" amount="$1.50" />
              <FeeRow label="IAS + MOAT + DV" value="$0.075/CPM" />
              <div className="border-t border-emerald-300 pt-2 mt-2">
                <FeeRow label="Total Supply Cost" value="29.0%" amount="$2.90" bold />
                <FeeRow label="Publisher Net" value="71.0%" amount="$7.10" bold />
              </div>
            </div>
          </div>
          <div className="bg-neutral-50 rounded-xl p-4 border border-neutral-200">
            <div className="text-xs font-semibold text-neutral-700 mb-3">TTD → Bidswitch → Magnite (Open Exchange)</div>
            <div className="space-y-2 font-mono text-xs">
              <FeeRow label="Luma Creative Gen" value={`$${lumaCpm.toFixed(4)}/CPM`} sub="amortized" />
              <FeeRow label="TTD Platform Fee" value="15.0%" amount="$1.50" />
              <FeeRow label="Bidswitch Exchange" value="2.0%" amount="$0.20" />
              <FeeRow label="Magnite SSP" value="15.0%" amount="$1.50" />
              <FeeRow label="IAS + MOAT + DV" value="$0.075/CPM" />
              <div className="border-t border-neutral-300 pt-2 mt-2">
                <FeeRow label="Total Supply Cost" value="32.0%" amount="$3.20" bold />
                <FeeRow label="Publisher Net" value="68.0%" amount="$6.80" bold />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Strategic Insight */}
      <div className="bg-neutral-900 rounded-2xl p-6 text-white">
        <h3 className="text-sm font-semibold mb-2">Strategic Insight</h3>
        <p className="text-sm text-neutral-300 leading-relaxed">
          Amazon DSP's post-June 2025 fee reduction saves <span className="font-semibold text-white">{adspSavingsVsTtd}%</span> in
          supply cost vs. The Trade Desk. On a $10 CPM, that's <span className="font-semibold text-white">${(10 * adspSavingsVsTtd / 100).toFixed(2)}</span> per
          thousand impressions freed up — more than enough to cover Luma Dream Machine creative generation
          costs at <span className="font-mono text-white">${lumaCpm.toFixed(4)}/CPM</span>.
        </p>
        <p className="text-sm text-neutral-400 mt-3">
          With {supplyPaths.length} activation paths across {dspComparison.length} DSPs — including Open Exchange, SmartSwitch, and Direct PMP deals —
          Luma captures value wherever the impression serves. ADSP's lower fees create the margin headroom;
          the breadth of SSP connectivity (Magnite, PubMatic, Index, Zeta, FreeWheel) ensures reach.
        </p>
      </div>

      {/* All Paths Table */}
      <div className="bg-white rounded-2xl p-6 border border-neutral-200">
        <h3 className="text-sm font-semibold text-neutral-900 mb-4">All Supply Paths ({supplyPaths.length})</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr className="text-left text-[10px] uppercase tracking-wider text-neutral-400">
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
                  <tr key={i} className={`border-t border-neutral-100 ${isAdsp ? 'bg-emerald-50' : ''}`}>
                    <td className="py-2 pr-3 text-neutral-700">{p.dsp}</td>
                    <td className="py-2 pr-3 text-neutral-500">{p.exchange}</td>
                    <td className="py-2 pr-3 text-neutral-500">{p.ssp}</td>
                    <td className="py-2 pr-3">
                      <span className={`text-[9px] font-medium px-1.5 py-0.5 rounded ${
                        p.dealType === 'PMP'
                          ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                          : 'bg-blue-50 text-blue-700 border border-blue-200'
                      }`}>{p.dealType}</span>
                    </td>
                    <td className="py-2 pr-3 text-neutral-700">{p.dspFee}%</td>
                    <td className="py-2 pr-3 text-neutral-500">{p.exchangeFee}%</td>
                    <td className="py-2 pr-3 text-neutral-500">{p.sspFee}%</td>
                    <td className="py-2 pr-3 text-neutral-800">{total}%</td>
                    <td className={`py-2 font-medium ${isAdsp ? 'text-emerald-700' : 'text-neutral-700'}`}>{net}%</td>
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
      <span className={`${highlight ? 'text-emerald-700' : 'text-neutral-600'}`}>
        {label}
        {sub && <span className="text-neutral-400 ml-1">({sub})</span>}
      </span>
      <div className="flex items-center gap-3">
        <span className="text-neutral-800">{value}</span>
        {amount && <span className="text-neutral-500 w-12 text-right">{amount}</span>}
      </div>
    </div>
  )
}
