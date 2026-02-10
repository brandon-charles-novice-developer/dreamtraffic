import { useState } from 'react'
import CampaignOverview from './components/CampaignOverview'
import CreativeStudio from './components/CreativeStudio'
import ApprovalWorkflow from './components/ApprovalWorkflow'
import VastInspector from './components/VastInspector'
import DSPDashboard from './components/DSPDashboard'
import SupplyChainMap from './components/SupplyChainMap'
import CampaignReport from './components/CampaignReport'

const tabs = [
  { id: 'overview', label: 'Campaign', icon: '◎' },
  { id: 'creative', label: 'Creative Studio', icon: '▶' },
  { id: 'approval', label: 'Approval', icon: '✓' },
  { id: 'vast', label: 'VAST Tag', icon: '⟨/⟩' },
  { id: 'dsp', label: 'DSP Trafficking', icon: '↗' },
  { id: 'supply', label: 'Supply Chain', icon: '⇄' },
  { id: 'report', label: 'Report', icon: '◈' },
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
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center text-sm font-bold">
              D
            </div>
            <div>
              <h1 className="text-base font-semibold text-white tracking-tight">DreamTraffic</h1>
              <p className="text-[10px] text-slate-500 tracking-wider uppercase">Luma AI Creative Pipeline</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              Pipeline Active
            </span>
          </div>
        </div>
      </header>

      {/* Tab Navigation */}
      <nav className="border-b border-slate-800 bg-slate-900/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="flex gap-1 overflow-x-auto py-1 -mb-px">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-1.5 px-3 py-2 text-xs font-medium rounded-t-lg transition-all whitespace-nowrap ${
                  activeTab === tab.id
                    ? 'bg-slate-800 text-white border-b-2 border-blue-500'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <span className="text-[10px]">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 py-6">
        <div className="animate-fade-in" key={activeTab}>
          <ActivePanel />
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 py-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 flex items-center justify-between text-[11px] text-slate-600">
          <span>Built with Claude Agent SDK + Luma Dream Machine</span>
          <span>DreamTraffic v0.1.0</span>
        </div>
      </footer>
    </div>
  )
}
