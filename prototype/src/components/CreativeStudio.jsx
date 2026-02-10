import { creatives } from '../data/creatives'

export default function CreativeStudio() {
  const creative = creatives[0]

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-neutral-900">Creative Studio</h2>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Video Player */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-neutral-200 overflow-hidden">
          <div className="relative bg-neutral-900 flex items-center justify-center" style={{ minHeight: '400px' }}>
            <video
              src={creative.videoUrl}
              controls
              loop
              playsInline
              className="max-h-[500px] w-auto"
              poster=""
            />
          </div>
          <div className="p-4 border-t border-neutral-200">
            <div className="flex items-center justify-between">
              <span className="text-sm font-semibold text-neutral-900">{creative.name}</span>
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-semibold bg-neutral-900 text-white">
                ACTIVE
              </span>
            </div>
            <p className="text-xs text-neutral-500 mt-1">Generated with Luma Dream Machine {creative.model}</p>
          </div>
        </div>

        {/* Specs & Details */}
        <div className="lg:col-span-3 space-y-4">
          <div className="bg-white rounded-2xl p-5 border border-neutral-200">
            <h3 className="text-sm font-semibold text-neutral-900 mb-3">Generation Details</h3>
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

          <div className="bg-white rounded-2xl p-5 border border-neutral-200">
            <h3 className="text-sm font-semibold text-neutral-900 mb-3">Dream Machine Prompt</h3>
            <div className="bg-neutral-50 rounded-xl p-4 border border-neutral-200">
              <p className="text-xs text-neutral-700 leading-relaxed font-mono">{creative.prompt}</p>
            </div>
          </div>

          <div className="bg-white rounded-2xl p-5 border border-neutral-200">
            <h3 className="text-sm font-semibold text-neutral-900 mb-3">Measurement Configuration</h3>
            <div className="flex flex-wrap gap-2">
              {creative.measurementVendors.map((v) => (
                <span
                  key={v}
                  className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs bg-neutral-100 text-neutral-700 border border-neutral-200"
                >
                  <span className="w-1 h-1 rounded-full bg-neutral-400" />
                  {v}
                </span>
              ))}
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs bg-neutral-900 text-white">
                OMID Compliant
              </span>
            </div>
          </div>

          <div className="bg-neutral-50 rounded-2xl p-5 border border-neutral-300">
            <p className="text-xs text-neutral-600 leading-relaxed">
              <span className="font-semibold text-neutral-900">Meta-demonstration:</span> This video was generated using Luma's own Dream Machine, then flowed through the DreamTraffic pipeline — compliance review, VAST 4.2 measurement wrapping, multi-DSP trafficking, and supply chain analysis. The product IS the demo.
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
      <div className="text-[10px] uppercase tracking-wider text-neutral-400">{label}</div>
      <div className={`text-sm text-neutral-800 mt-0.5 ${mono ? 'font-mono text-xs' : ''}`}>{value}</div>
    </div>
  )
}
