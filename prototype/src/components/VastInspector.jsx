import { vastXml, trackingEvents, measurementVendors } from '../data/vastXml'

function highlightXml(xml) {
  return xml
    .replace(/(&lt;|<)(\/?)([\w][\w-]*)/g, '$1$2<span class="tag">$3</span>')
    .replace(/([\w][\w-]*)(\s*=\s*)"([^"]*)"/g, '<span class="attr">$1</span>$2"<span class="value">$3</span>"')
    .replace(/(https?:\/\/[^\s<&]+)/g, '<span class="text">$1</span>')
}

export default function VastInspector() {
  const lines = vastXml.split('\n')

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-neutral-900">VAST 4.2 Tag Inspector</h2>
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[11px] font-semibold bg-neutral-900 text-white">
          OMID Compliant
        </span>
      </div>

      {/* VAST XML */}
      <div className="bg-white rounded-2xl border border-neutral-200 overflow-hidden">
        <div className="flex items-center justify-between px-4 py-2.5 border-b border-neutral-200 bg-neutral-50">
          <span className="text-xs font-medium text-neutral-700">VAST 4.2 InLine Tag</span>
          <div className="flex items-center gap-2">
            <span className="text-[10px] text-neutral-400">dt-842e3cf0f0d6</span>
            <button
              onClick={() => navigator.clipboard.writeText(vastXml)}
              className="text-[10px] text-neutral-500 hover:text-neutral-900 transition-colors px-2 py-0.5 rounded bg-neutral-200 hover:bg-neutral-300"
            >
              Copy XML
            </button>
          </div>
        </div>
        <div className="overflow-x-auto">
          <pre className="vast-xml p-4 leading-relaxed bg-neutral-50">
            {lines.map((line, i) => (
              <div key={i} className="flex">
                <span className="select-none text-neutral-300 w-8 text-right mr-4 flex-shrink-0">{i + 1}</span>
                <span dangerouslySetInnerHTML={{ __html: highlightXml(escapeHtml(line)) }} />
              </div>
            ))}
          </pre>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Measurement Vendors */}
        <div className="bg-white rounded-2xl p-5 border border-neutral-200">
          <h3 className="text-sm font-semibold text-neutral-900 mb-4">AdVerification Vendors</h3>
          <div className="space-y-3">
            {measurementVendors.map((v) => (
              <div key={v.key} className="flex items-center justify-between py-2 border-b border-neutral-100 last:border-0">
                <div>
                  <div className="text-sm text-neutral-800">{v.name}</div>
                  <div className="text-xs text-neutral-500 mt-0.5">{v.type}</div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-mono text-neutral-800">${v.cpm.toFixed(3)}</div>
                  <div className="text-[10px] text-neutral-400">CPM</div>
                </div>
              </div>
            ))}
            <div className="flex items-center justify-between pt-2 border-t border-neutral-300">
              <span className="text-xs font-medium text-neutral-700">Total Measurement CPM</span>
              <span className="text-sm font-mono font-semibold text-neutral-900">
                ${measurementVendors.reduce((sum, v) => sum + v.cpm, 0).toFixed(3)}
              </span>
            </div>
          </div>
        </div>

        {/* Tracking Events */}
        <div className="bg-white rounded-2xl p-5 border border-neutral-200">
          <h3 className="text-sm font-semibold text-neutral-900 mb-4">TrackingEvents</h3>
          <div className="space-y-2">
            {trackingEvents.map((te) => (
              <div key={te.event} className="flex items-center gap-3">
                <div className="w-6 h-6 rounded bg-neutral-100 flex items-center justify-center text-xs">
                  {te.icon}
                </div>
                <div className="flex-1">
                  <span className="text-xs font-mono text-neutral-700">{te.event}</span>
                </div>
                <span className="text-[11px] text-neutral-500">{te.description}</span>
              </div>
            ))}
          </div>
          <div className="mt-4 pt-3 border-t border-neutral-100">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              <span className="text-xs text-neutral-500">All events firing with cache-busting macros</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}
