# DreamTraffic

Full-stack creative pipeline for **Luma AI Dream Machine** — from AI video generation through programmatic trafficking, measurement wrapping, and supply chain analysis.

## What This Demonstrates

The complete lifecycle of a video creative in programmatic advertising:

1. **Creative Generation** — Luma Dream Machine API generates placement-optimized video
2. **Compliance Review** — Validates against IAB/DSP specs (duration, resolution, format)
3. **Measurement Wrapping** — VAST 4.2 with IAS, MOAT, DoubleVerify AdVerification (OMID)
4. **DSP Trafficking** — Upload to Amazon DSP, TTD, DV360, StackAdapt, Adelphic
5. **Exchange Routing** — Bidswitch T-Groups and SmartSwitch ML scoring
6. **SSP Delivery** — Magnite, PubMatic, Index Exchange, FreeWheel (OpenRTB 2.6)
7. **Fee Stack Analysis** — Full supply chain economics with ADSP advantage modeling

## The Strategic Insight

Amazon DSP's post-June 2025 fee reductions (managed-service cut to 12%) create margin headroom in the supply chain. That freed budget is exactly where Luma AI captures value — premium AI-generated creative that previously couldn't justify its cost against tight programmatic margins.

## Architecture

Built with the **Claude Agent SDK** using four specialized agents:

| Agent | Model | Role |
|-------|-------|------|
| Creative Director | Sonnet | Campaign brief → Luma-optimized prompts → video generation |
| Compliance Reviewer | Haiku | IAB/DSP spec validation, measurement requirements |
| Trafficking Manager | Sonnet | VAST generation, multi-DSP upload, audit tracking |
| Supply Chain Analyst | Haiku | Fee stacks, supply path optimization, ADSP advantage |

Each agent uses custom MCP tools (22 total) backed by SQLite, real VAST 4.2 XML generation, and simulated DSP/exchange/SSP integrations.

## Quick Start

```bash
# Install
uv sync

# Initialize database with seed data
dreamtraffic init-db

# Run the full demo pipeline (no API keys needed)
dreamtraffic demo

# View pipeline status
dreamtraffic status
```

## CLI Commands

```bash
# Generate video with Luma (requires LUMAAI_API_KEY)
dreamtraffic generate --campaign-id 1 --prompt "Cinematic aerial shot..." --placement stv

# Generate VAST 4.2 tag with measurement vendors
dreamtraffic vast --creative-id 1 --vendors ias,moat,doubleverify

# Traffic to DSPs (simulated)
dreamtraffic traffic --creative-id 1 --dsp amazon --dsp thetradedesk --dsp dv360

# Analyze supply chain fee stacks
dreamtraffic supply-chain --base-cpm 10.0

# Manage approval workflow
dreamtraffic approve --creative-id 1 --action submit
dreamtraffic approve --creative-id 1 --action approve
```

## Real vs. Simulated

| Component | Status |
|-----------|--------|
| Luma Dream Machine API | **Real** (requires API key) |
| Claude Agent SDK agents | **Real** (requires Anthropic API key) |
| SQLite database (6 tables) | **Real** |
| VAST 4.2 XML with OMID AdVerification | **Real** — valid, parseable XML |
| Approval state machine | **Real** |
| Fee stack calculator | **Real** |
| DSP integrations | Simulated (returns `_simulated: true`) |
| Bidswitch exchange routing | Simulated |
| SSP OpenRTB 2.6 | Simulated |

All simulated components include `PRODUCTION NOTE` comments describing what real integration would require.

## Supply Chain Economics

```
ADSP Path (post-June 2025):
  Luma Creative Gen    $0.0050/CPM (amortized)
  Amazon DSP Fee       12.0%
  Bidswitch Exchange   2.0%
  Magnite SSP          15.0%
  IAS + MOAT + DV      $0.075/CPM
  ─────────────────────────────
  Total Supply Cost    29.0% + measurement
  Publisher Net        71.0%

TTD Path:
  Total Supply Cost    32.0% + measurement
  Publisher Net        68.0%

ADSP Advantage: 3% lower supply cost → margin for Luma creative generation
```

## Testing

```bash
uv sync --extra dev
pytest --cov
```
