export const supplyPaths = [
  { dsp: 'Amazon DSP', exchange: 'Bidswitch', ssp: 'Magnite', dspFee: 12, exchangeFee: 2, sspFee: 15, measurementCpm: 0.02, winRate: 0.18, latency: 85, notes: 'Certified Supply Exchange partner' },
  { dsp: 'Amazon DSP', exchange: 'Bidswitch', ssp: 'PubMatic', dspFee: 12, exchangeFee: 2, sspFee: 14, measurementCpm: 0.02, winRate: 0.15, latency: 90, notes: 'Cloud infra, OpenWrap' },
  { dsp: 'Amazon DSP', exchange: 'Bidswitch', ssp: 'Index Exchange', dspFee: 12, exchangeFee: 2, sspFee: 12, measurementCpm: 0.02, winRate: 0.20, latency: 75, notes: 'Header bidding transparency' },
  { dsp: 'Amazon DSP', exchange: 'Direct', ssp: 'FreeWheel', dspFee: 12, exchangeFee: 0, sspFee: 18, measurementCpm: 0.02, winRate: 0.12, latency: 95, notes: 'Premium streaming pods' },
  { dsp: 'The Trade Desk', exchange: 'Bidswitch', ssp: 'Magnite', dspFee: 15, exchangeFee: 2, sspFee: 15, measurementCpm: 0.03, winRate: 0.16, latency: 88, notes: 'Premium video' },
  { dsp: 'The Trade Desk', exchange: 'Bidswitch', ssp: 'PubMatic', dspFee: 15, exchangeFee: 2, sspFee: 14, measurementCpm: 0.03, winRate: 0.14, latency: 92, notes: 'Standard path' },
  { dsp: 'The Trade Desk', exchange: 'Bidswitch', ssp: 'Index Exchange', dspFee: 15, exchangeFee: 2, sspFee: 12, measurementCpm: 0.03, winRate: 0.19, latency: 78, notes: 'Header bidding' },
  { dsp: 'DV360', exchange: 'Bidswitch', ssp: 'Magnite', dspFee: 14, exchangeFee: 2, sspFee: 15, measurementCpm: 0.025, winRate: 0.15, latency: 90, notes: 'Via Bidswitch' },
  { dsp: 'DV360', exchange: 'Direct', ssp: 'FreeWheel', dspFee: 14, exchangeFee: 0, sspFee: 18, measurementCpm: 0.025, winRate: 0.10, latency: 98, notes: 'Google-preferred path' },
]

export const dspComparison = [
  { dsp: 'Amazon DSP', avgDspFee: 12.0, avgTotalCost: 28.25, avgPublisherNet: 71.75, paths: 4, highlight: true },
  { dsp: 'The Trade Desk', avgDspFee: 15.0, avgTotalCost: 30.67, avgPublisherNet: 69.33, paths: 3, highlight: false },
  { dsp: 'DV360', avgDspFee: 14.0, avgTotalCost: 31.5, avgPublisherNet: 68.5, paths: 2, highlight: false },
]

export const lumaCpm = 0.005 // $0.005 per 1000 impressions (amortized)
export const adspSavingsVsTtd = 2.42 // percentage points
