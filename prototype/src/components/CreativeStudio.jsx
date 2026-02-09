import { creatives } from '../data/creatives'

export default function CreativeStudio() {
  const creative = creatives[0]

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-white">Creative Studio</h2>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Video Player — takes 2 columns */}
        <div className="lg:col-span-2 bg-slate-800/50 rounded-xl border border-slate-700/50 overflow-hidden">
          <div className="relative bg-black flex items-center justify-center" style={{ minHeight: '400px' }}>
            <video
              src={creative.videoUrl}
              controls
              loop
              playsInline
              className="max-h-[500px] w-auto"
              poster=""
            />
          </div>
          <div className="p-4 border-t border-slate-700/50">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-white">{creative.name}</span>
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                ACTIVE
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">Generated with Luma Dream Machine {creative.model}</p>
          </div>
        </div>

        {/* Specs & Details — takes 3 columns */}
        <div className="lg:col-span-3 space-y-4">
          {/* Generation Details */}
          <div className="bg-slate-800/50 rounded-xl p-5 border border-slate-700/50">
            <h3 className="text-sm font-semibold text-white mb-3">Generation Details</h3>
            <div className="grid grid-cols-2 gap-3">
              <Spec label="Model" value={`Dream Machine ${creative.model}`} />
              <Spec label="Generation ID" value={creative.lumaGenerationId} mono />
              <Spec label="Duration" value={`${creative.duration}s`} />
              <Spec label="Resolution" value={`${creative.width}x${creative.height}`} />
              <Spec label="Aspect Ratio" value={creative.aspectRatio} />
              <Spec label="Format" value={`${creative.format.toUpperCase()} (${creative.codec})`} />
              <Spec label="File Size" value={creative.fileSize} />
              <Spec label="Placement" value={creative.placementType} />
            </div>
          </div>

          {/* Prompt */}
          <div className="bg-slate-800/50 rounded-xl p-5 border border-slate-700/50">
            <h3 className="text-sm font-semibold text-white mb-3">Dream Machine Prompt</h3>
            <div className="bg-slate-900/80 rounded-lg p-4 border border-slate-700/30">
              <p className="text-xs text-slate-300 leading-relaxed font-mono">{creative.prompt}</p>
            </div>
          </div>

          {/* Measurement */}
          <div className="bg-slate-800/50 rounded-xl p-5 border border-slate-700/50">
            <h3 className="text-sm font-semibold text-white mb-3">Measurement Configuration</h3>
            <div className="flex flex-wrap gap-2">
              {creative.measurementVendors.map((v) => (
                <span
                  key={v}
                  className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs bg-blue-500/10 text-blue-300 border border-blue-500/20"
                >
                  <span className="w-1 h-1 rounded-full bg-blue-400" />
                  {v}
                </span>
              ))}
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs bg-violet-500/10 text-violet-300 border border-violet-500/20">
                OMID Compliant
              </span>
            </div>
          </div>

          {/* Meta Note */}
          <div className="bg-gradient-to-r from-blue-500/5 to-violet-500/5 rounded-xl p-5 border border-blue-500/20">
            <p className="text-xs text-blue-300 leading-relaxed">
              <span className="font-semibold text-blue-200">Meta-demonstration:</span> This video was generated using Luma's own Dream Machine, then flowed through the DreamTraffic pipeline — compliance review, VAST 4.2 measurement wrapping, multi-DSP trafficking, and supply chain analysis. The product IS the demo.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

function Spec({ label, value, mono }) {
  return (
    <div>
      <div className="text-[10px] uppercase tracking-wider text-slate-500">{label}</div>
      <div className={`text-sm text-slate-200 mt-0.5 ${mono ? 'font-mono text-xs' : ''}`}>{value}</div>
    </div>
  )
}
