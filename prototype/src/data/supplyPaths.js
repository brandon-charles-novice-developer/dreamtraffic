export const supplyPaths = [
  // Amazon DSP paths
  { dsp: 'Amazon DSP', exchange: 'Bidswitch', ssp: 'Magnite', dealType: 'Open Exchange', dspFee: 12, exchangeFee: 2, sspFee: 15, measurementCpm: 0.02, winRate: 0.18, latency: 85, notes: 'Certified Supply Exchange partner' },
  { dsp: 'Amazon DSP', exchange: 'Bidswitch', ssp: 'PubMatic', dealType: 'Open Exchange', dspFee: 12, exchangeFee: 2, sspFee: 14, measurementCpm: 0.02, winRate: 0.15, latency: 90, notes: 'Cloud infra, OpenWrap' },
  { dsp: 'Amazon DSP', exchange: 'Bidswitch', ssp: 'Index Exchange', dealType: 'Open Exchange', dspFee: 12, exchangeFee: 2, sspFee: 12, measurementCpm: 0.02, winRate: 0.20, latency: 75, notes: 'Header bidding transparency' },
  { dsp: 'Amazon DSP', exchange: 'SmartSwitch', ssp: 'Zeta Global', dealType: 'PMP', dspFee: 12, exchangeFee: 1.5, sspFee: 13, measurementCpm: 0.02, winRate: 0.17, latency: 80, notes: 'Data-driven PMP, identity graph' },
  { dsp: 'Amazon DSP', exchange: 'Direct', ssp: 'FreeWheel', dealType: 'PMP', dspFee: 12, exchangeFee: 0, sspFee: 18, measurementCpm: 0.02, winRate: 0.12, latency: 95, notes: 'Premium streaming pods' },
  // The Trade Desk paths
  { dsp: 'The Trade Desk', exchange: 'Bidswitch', ssp: 'Magnite', dealType: 'Open Exchange', dspFee: 15, exchangeFee: 2, sspFee: 15, measurementCpm: 0.03, winRate: 0.16, latency: 88, notes: 'Premium video' },
  { dsp: 'The Trade Desk', exchange: 'Bidswitch', ssp: 'PubMatic', dealType: 'Open Exchange', dspFee: 15, exchangeFee: 2, sspFee: 14, measurementCpm: 0.03, winRate: 0.14, latency: 92, notes: 'Standard path' },
  { dsp: 'The Trade Desk', exchange: 'Bidswitch', ssp: 'Index Exchange', dealType: 'Open Exchange', dspFee: 15, exchangeFee: 2, sspFee: 12, measurementCpm: 0.03, winRate: 0.19, latency: 78, notes: 'Header bidding' },
  { dsp: 'The Trade Desk', exchange: 'SmartSwitch', ssp: 'Zeta Global', dealType: 'PMP', dspFee: 15, exchangeFee: 1.5, sspFee: 13, measurementCpm: 0.03, winRate: 0.15, latency: 82, notes: 'UID 2.0 + Zeta identity' },
  // DV360 paths
  { dsp: 'DV360', exchange: 'Bidswitch', ssp: 'Magnite', dealType: 'Open Exchange', dspFee: 14, exchangeFee: 2, sspFee: 15, measurementCpm: 0.025, winRate: 0.15, latency: 90, notes: 'Via Bidswitch' },
  { dsp: 'DV360', exchange: 'Direct', ssp: 'FreeWheel', dealType: 'PMP', dspFee: 14, exchangeFee: 0, sspFee: 18, measurementCpm: 0.025, winRate: 0.10, latency: 98, notes: 'Google-preferred path' },
  // Challenger DSP paths
  { dsp: 'StackAdapt', exchange: 'Bidswitch', ssp: 'Magnite', dealType: 'Open Exchange', dspFee: 16, exchangeFee: 2.5, sspFee: 15, measurementCpm: 0.03, winRate: 0.12, latency: 95, notes: 'Contextual targeting' },
  { dsp: 'StackAdapt', exchange: 'SmartSwitch', ssp: 'Zeta Global', dealType: 'PMP', dspFee: 16, exchangeFee: 2, sspFee: 13, measurementCpm: 0.03, winRate: 0.10, latency: 88, notes: 'Household-level reach' },
  { dsp: 'Adelphic / Viant', exchange: 'Bidswitch', ssp: 'PubMatic', dealType: 'Open Exchange', dspFee: 16, exchangeFee: 2.5, sspFee: 14, measurementCpm: 0.03, winRate: 0.11, latency: 93, notes: 'Viant Household ID graph' },
]

export const dspComparison = [
  { dsp: 'Amazon DSP', avgDspFee: 12.0, avgTotalCost: 27.7, avgPublisherNet: 72.3, paths: 5, highlight: true },
  { dsp: 'The Trade Desk', avgDspFee: 15.0, avgTotalCost: 30.38, avgPublisherNet: 69.63, paths: 4, highlight: false },
  { dsp: 'DV360', avgDspFee: 14.0, avgTotalCost: 31.5, avgPublisherNet: 68.5, paths: 2, highlight: false },
  { dsp: 'StackAdapt', avgDspFee: 16.0, avgTotalCost: 32.25, avgPublisherNet: 67.75, paths: 2, highlight: false },
  { dsp: 'Adelphic / Viant', avgDspFee: 16.0, avgTotalCost: 32.5, avgPublisherNet: 67.5, paths: 1, highlight: false },
]

export const lumaCpm = 0.005 // $0.005 per 1000 impressions (amortized)
export const adspSavingsVsTtd = 2.42 // percentage points
