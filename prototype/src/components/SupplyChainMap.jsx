import { supplyPaths, dspComparison, lumaCpm, adspSavingsVsTtd } from '../data/supplyPaths'

export default function SupplyChainMap() {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-white">Supply Chain Map</h2>

      {/* Visual Flow */}
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <h3 className="text-sm font-semibold text-white mb-5">Programmatic Supply Chain Flow</h3>
        <div className="flex items-center justify-between gap-2 overflow-x-auto pb-2">
          {[
            { label: 'Luma AI', sub: 'Dream Machine', color: 'from-blue-500 to-violet-500' },
            { label: 'DSP', sub: 'ADSP / TTD / DV360', color: 'from-amber-500 to-orange-500' },
            { label: 'Bidswitch', sub: 'T-Groups + SmartSwitch', color: 'from-cyan-500 to-blue-500' },
            { label: 'SSP', sub: 'Magnite / PubMatic / Index', color: 'from-emerald-500 to-teal-500' },
            { label: 'Publisher', sub: 'Impression Served', color: 'from-pink-500 to-rose-500' },
          ].map((node, i, arr) => (
            <div key={node.label} className="flex items-center gap-2 flex-shrink-0">
              <div className="flex flex-col items-center">
                <div className={`w-20 h-20 rounded-2xl bg-gradient-to-br ${node.color} flex items-center justify-center shadow-lg`}>
                  <span className="text-white text-xs font-bold text-center leading-tight">{node.label}</span>
                </div>
                <span className="text-[10px] text-slate-400 mt-2 text-center max-w-[90px]">{node.sub}</span>
              </div>
              {i < arr.length - 1 && (
                <div className="flex items-center -mt-6">
                  <div className="w-8 h-px bg-gradient-to-r from-slate-500 to-slate-600" />
                  <span className="text-slate-500 text-xs">→</span>
                  <div className="w-8 h-px bg-gradient-to-r from-slate-600 to-slate-500" />
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* DSP Comparison */}
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <h3 className="text-sm font-semibold text-white mb-4">DSP Fee Comparison</h3>
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
            <div className="text-xs font-semibold text-emerald-300 mb-3">Amazon DSP → Bidswitch → Magnite</div>
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
            <div className="text-xs font-semibold text-slate-300 mb-3">TTD → Bidswitch → Magnite</div>
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
          This is where Luma captures value in the supply chain: ADSP's lower fees create margin headroom
          for premium AI-generated creative that wasn't economically viable at higher fee structures.
        </p>
      </div>

      {/* All Paths Table */}
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <h3 className="text-sm font-semibold text-white mb-4">All Supply Paths</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr className="text-left text-[10px] uppercase tracking-wider text-slate-500">
                <th className="pb-2 pr-3">DSP</th>
                <th className="pb-2 pr-3">Exchange</th>
                <th className="pb-2 pr-3">SSP</th>
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
