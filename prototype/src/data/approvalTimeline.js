export const approvalTimeline = [
  {
    fromStatus: 'draft',
    toStatus: 'pending_review',
    reviewer: 'Creative Director',
    notes: 'Submitted for compliance review — 6s social variant from Dream Machine Ray2',
    timestamp: '2026-02-09T10:15:00Z',
  },
  {
    fromStatus: 'pending_review',
    toStatus: 'approved',
    reviewer: 'Compliance Reviewer',
    notes: 'All DSP specs validated. OMID-compliant AdVerification confirmed for IAS, MOAT, DoubleVerify. Duration within social video limits. H.264 codec verified.',
    timestamp: '2026-02-09T10:18:00Z',
  },
  {
    fromStatus: 'approved',
    toStatus: 'trafficked',
    reviewer: 'Trafficking Manager',
    notes: 'VAST 4.2 tag generated with full measurement wrapping. Uploaded to Amazon DSP, The Trade Desk, and DV360.',
    timestamp: '2026-02-09T10:22:00Z',
  },
  {
    fromStatus: 'trafficked',
    toStatus: 'active',
    reviewer: 'System',
    notes: 'DSP audits passed across all platforms. Creative now serving impressions.',
    timestamp: '2026-02-09T10:45:00Z',
  },
]

export const complianceChecks = [
  { check: 'IAB Duration Validation', status: 'pass', detail: '6s within 6-30s range for social video' },
  { check: 'Resolution Check', status: 'pass', detail: '720x1280 meets minimum 640x360 for OLV' },
  { check: 'Codec Validation', status: 'pass', detail: 'H.264 + AAC — universal DSP compatibility' },
  { check: 'File Size', status: 'pass', detail: '2.8 MB within 500 MB limit' },
  { check: 'VAST 4.2 Structure', status: 'pass', detail: 'InLine tag with AdVerifications, TrackingEvents, VideoClicks' },
  { check: 'OMID Compliance', status: 'pass', detail: 'AdVerification elements with apiFramework="omid" for all 3 vendors' },
  { check: 'Measurement Vendors', status: 'pass', detail: 'IAS, MOAT, DoubleVerify — all configured with VerificationParameters' },
  { check: 'Tracking Events', status: 'pass', detail: 'Full quartile tracking: start → 25% → 50% → 75% → complete' },
]
