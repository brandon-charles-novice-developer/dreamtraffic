import { useState } from 'react'
import CampaignOverview from './components/CampaignOverview'
import CreativeStudio from './components/CreativeStudio'
import ApprovalWorkflow from './components/ApprovalWorkflow'
import VastInspector from './components/VastInspector'
import DSPDashboard from './components/DSPDashboard'
import SupplyChainMap from './components/SupplyChainMap'
import CampaignReport from './components/CampaignReport'

const tabs = [
  { id: 'overview', label: 'Campaign' },
  { id: 'creative', label: 'Creative Studio' },
  { id: 'approval', label: 'Approval' },
  { id: 'vast', label: 'VAST Tag' },
  { id: 'dsp', label: 'DSP Trafficking' },
  { id: 'supply', label: 'Supply Chain' },
  { id: 'report', label: 'Report' },
]

const panels = {
  overview: CampaignOverview,
  creative: CreativeStudio,
  approval: ApprovalWorkflow,
  vast: VastInspector,
  dsp: DSPDashboard,
  supply: SupplyChainMap,
  report: CampaignReport,
}

export default function App() {
  const [activeTab, setActiveTab] = useState('overview')
  const ActivePanel = panels[activeTab]

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header — Luma-style */}
      <header className="bg-white border-b border-neutral-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-lg">🌙</span>
            <span className="text-base font-bold tracking-tight text-neutral-900">Luma Dream Traffic Machine</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-neutral-900 text-white">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              Pipeline Active
            </span>
          </div>
        </div>
      </header>

      {/* Tab Navigation — Luma uppercase style */}
      <nav className="bg-white border-b border-neutral-200">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex gap-0 overflow-x-auto -mb-px">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-3 text-xs font-semibold uppercase tracking-wider transition-all whitespace-nowrap border-b-2 ${
                  activeTab === tab.id
                    ? 'border-neutral-900 text-neutral-900'
                    : 'border-transparent text-neutral-400 hover:text-neutral-700'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-6 py-8">
        <div className="animate-fade-in" key={activeTab}>
          <ActivePanel />
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-neutral-200 bg-white py-4">
        <div className="max-w-7xl mx-auto px-6 flex items-center justify-between text-xs text-neutral-400">
          <span>Luma Dream Traffic Machine</span>
          <span>v0.1.0</span>
        </div>
      </footer>
    </div>
  )
}
