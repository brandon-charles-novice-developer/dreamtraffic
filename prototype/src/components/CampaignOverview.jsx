import { campaign } from '../data/campaign'

function Field({ label, value }) {
  return (
    <div>
      <dt className="text-[11px] uppercase tracking-wider text-neutral-400 mb-1">{label}</dt>
      <dd className="text-sm text-neutral-800">{value}</dd>
    </div>
  )
}

export default function CampaignOverview() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-neutral-900">{campaign.name}</h2>
          <p className="text-sm text-neutral-500 mt-1">{campaign.advertiser}</p>
        </div>
        <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium bg-neutral-900 text-white">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
          Active
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-2xl p-5 border border-neutral-200">
          <div className="text-2xl font-bold text-neutral-900">${(campaign.budget / 1000).toFixed(0)}K</div>
          <div className="text-xs text-neutral-500 mt-1">Campaign Budget</div>
        </div>
        <div className="bg-white rounded-2xl p-5 border border-neutral-200">
          <div className="text-2xl font-bold text-neutral-900">5</div>
          <div className="text-xs text-neutral-500 mt-1">DSPs Trafficking</div>
        </div>
        <div className="bg-white rounded-2xl p-5 border border-neutral-200">
          <div className="text-2xl font-bold text-neutral-900">3</div>
          <div className="text-xs text-neutral-500 mt-1">Measurement Vendors</div>
        </div>
      </div>

      <div className="bg-white rounded-2xl p-6 border border-neutral-200">
        <h3 className="text-sm font-semibold text-neutral-900 mb-4">Campaign Details</h3>
        <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-4">
          <Field label="Objective" value={campaign.objective} />
          <Field label="Audience" value={campaign.audience} />
          <Field label="Placements" value={campaign.placements.join(', ')} />
          <Field label="Flight Dates" value={`${campaign.flightStart} → ${campaign.flightEnd}`} />
        </dl>
      </div>

      <div className="bg-white rounded-2xl p-6 border border-neutral-200">
        <h3 className="text-sm font-semibold text-neutral-900 mb-3">Campaign Brief</h3>
        <p className="text-sm text-neutral-600 leading-relaxed">{campaign.brief}</p>
      </div>

      {/* Pipeline Status */}
      <div className="bg-white rounded-2xl p-6 border border-neutral-200">
        <h3 className="text-sm font-semibold text-neutral-900 mb-4">Pipeline Status</h3>
        <div className="flex items-center gap-2">
          {['Generation', 'Review', 'VAST Wrapping', 'Trafficking', 'Active'].map((step, i) => (
            <div key={step} className="flex items-center gap-2 flex-1">
              <div className="flex flex-col items-center flex-1">
                <div className="w-8 h-8 rounded-full bg-neutral-900 flex items-center justify-center text-white text-xs font-bold">
                  ✓
                </div>
                <span className="text-[10px] text-neutral-500 mt-1.5 text-center">{step}</span>
              </div>
              {i < 4 && <div className="h-px flex-1 bg-neutral-300 -mt-4" />}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
