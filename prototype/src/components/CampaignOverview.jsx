import { campaign } from '../data/campaign'

function Field({ label, value }) {
  return (
    <div>
      <dt className="text-[11px] uppercase tracking-wider text-slate-500 mb-1">{label}</dt>
      <dd className="text-sm text-slate-200">{value}</dd>
    </div>
  )
}

export default function CampaignOverview() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-white">{campaign.name}</h2>
          <p className="text-sm text-slate-400 mt-1">{campaign.advertiser}</p>
        </div>
        <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
          Active
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-800/50 rounded-xl p-5 border border-slate-700/50">
          <div className="text-2xl font-bold text-white">${(campaign.budget / 1000).toFixed(0)}K</div>
          <div className="text-xs text-slate-400 mt-1">Campaign Budget</div>
        </div>
        <div className="bg-slate-800/50 rounded-xl p-5 border border-slate-700/50">
          <div className="text-2xl font-bold text-white">5</div>
          <div className="text-xs text-slate-400 mt-1">DSPs Trafficking</div>
        </div>
        <div className="bg-slate-800/50 rounded-xl p-5 border border-slate-700/50">
          <div className="text-2xl font-bold text-white">3</div>
          <div className="text-xs text-slate-400 mt-1">Measurement Vendors</div>
        </div>
      </div>

      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <h3 className="text-sm font-semibold text-white mb-4">Campaign Details</h3>
        <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-4">
          <Field label="Objective" value={campaign.objective} />
          <Field label="Audience" value={campaign.audience} />
          <Field label="Placements" value={campaign.placements.join(', ')} />
          <Field label="Flight Dates" value={`${campaign.flightStart} → ${campaign.flightEnd}`} />
        </dl>
      </div>

      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <h3 className="text-sm font-semibold text-white mb-3">Campaign Brief</h3>
        <p className="text-sm text-slate-300 leading-relaxed">{campaign.brief}</p>
      </div>

      {/* Pipeline Status */}
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
        <h3 className="text-sm font-semibold text-white mb-4">Pipeline Status</h3>
        <div className="flex items-center gap-2">
          {['Generation', 'Review', 'VAST Wrapping', 'Trafficking', 'Active'].map((step, i) => (
            <div key={step} className="flex items-center gap-2 flex-1">
              <div className="flex flex-col items-center flex-1">
                <div className="w-8 h-8 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400 text-xs font-bold">
                  ✓
                </div>
                <span className="text-[10px] text-slate-400 mt-1.5 text-center">{step}</span>
              </div>
              {i < 4 && <div className="h-px flex-1 bg-emerald-500/30 -mt-4" />}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
