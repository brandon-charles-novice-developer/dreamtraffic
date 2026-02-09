"""Click CLI — orchestrates the full DreamTraffic pipeline."""

from __future__ import annotations

import asyncio
import json

import click
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax

from dreamtraffic.db.migrations import init_db
from dreamtraffic.db.engine import fetch_one, fetch_all, execute
from dreamtraffic.luma.client import LumaClient
from dreamtraffic.measurement.vast import VastGenerator
from dreamtraffic.measurement.fee_stack import FeeStackCalculator
from dreamtraffic.dsp import get_adapter
from dreamtraffic.exchange.bidswitch import BidswitchRouter
from dreamtraffic.approval.workflow import ApprovalWorkflow
from dreamtraffic.approval.notifications import format_timeline

console = Console()


@click.group()
def cli():
    """DreamTraffic — Full-stack creative pipeline for Luma AI Dream Machine."""
    pass


@cli.command("init-db")
def cmd_init_db():
    """Initialize the database with tables and seed data."""
    init_db()
    console.print("[green]Database initialized with seed data.[/green]")
    specs = fetch_all("SELECT COUNT(*) as count FROM dsp_specs")
    paths = fetch_all("SELECT COUNT(*) as count FROM supply_paths")
    console.print(f"  DSP specs: {specs[0]['count']} records")
    console.print(f"  Supply paths: {paths[0]['count']} records")


@cli.command("generate")
@click.option("--campaign-id", type=int, required=True, help="Campaign ID")
@click.option("--prompt", required=True, help="Luma Dream Machine prompt")
@click.option("--duration", default="5s", help="Video duration (e.g., 5s)")
@click.option("--resolution", default="1080p", help="Video resolution")
@click.option("--name", default="", help="Creative name")
@click.option("--placement", default="olv", type=click.Choice(["olv", "stv", "preroll"]))
@click.option("--wait/--no-wait", default=True, help="Wait for generation to complete")
def cmd_generate(campaign_id, prompt, duration, resolution, name, placement, wait):
    """Generate a video creative using Luma Dream Machine."""
    campaign = fetch_one("SELECT * FROM campaigns WHERE id = ?", (campaign_id,))
    if campaign is None:
        console.print(f"[red]Campaign {campaign_id} not found. Run init-db first.[/red]")
        return

    client = LumaClient()
    console.print(f"[yellow]Starting Luma generation...[/yellow]")
    console.print(f"  Prompt: {prompt[:80]}...")

    if wait:
        with console.status("Generating video with Luma Dream Machine..."):
            result = client.generate_and_wait(
                prompt, duration=duration, resolution=resolution
            )
        video_url = result["video_url"]
        console.print(f"[green]Generation complete![/green]")
        console.print(f"  Video URL: {video_url}")
    else:
        gen_id = client.generate(prompt, duration=duration, resolution=resolution)
        video_url = ""
        console.print(f"  Generation ID: {gen_id}")
        console.print("  Use 'poll' command to check status.")
        result = {"id": gen_id}

    # Create creative record
    dur_secs = int(duration.replace("s", "")) if "s" in duration else 30
    cursor = execute(
        """INSERT INTO creatives (campaign_id, name, prompt, luma_generation_id,
           video_url, duration_seconds, placement_type)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (campaign_id, name or f"Creative-{placement}", prompt,
         result.get("id", ""), video_url, dur_secs, placement),
    )
    console.print(f"  Creative ID: {cursor.lastrowid}")


@cli.command("vast")
@click.option("--creative-id", type=int, required=True, help="Creative ID")
@click.option("--vendors", default="ias,moat,doubleverify", help="Comma-separated vendor keys")
@click.option("--wrapper", is_flag=True, help="Generate wrapper tag instead of inline")
def cmd_vast(creative_id, vendors, wrapper):
    """Generate a VAST 4.2 tag with measurement vendor wrapping."""
    creative = fetch_one("SELECT * FROM creatives WHERE id = ?", (creative_id,))
    if creative is None:
        console.print(f"[red]Creative {creative_id} not found.[/red]")
        return

    vendor_list = [v.strip() for v in vendors.split(",")]
    generator = VastGenerator()

    if wrapper:
        if not creative["vast_url"]:
            console.print("[red]No existing VAST URL to wrap. Generate inline first.[/red]")
            return
        xml = generator.generate_wrapper(
            vast_ad_tag_uri=creative["vast_url"],
            vendors=vendor_list,
        )
    else:
        secs = creative["duration_seconds"]
        xml = generator.generate_inline(
            video_url=creative["video_url"] or "https://cdn.luma.example/demo.mp4",
            duration=f"00:00:{secs:02d}",
            title=creative["name"],
            vendors=vendor_list,
        )
        # Store VAST URL
        vast_url = f"https://vast.dreamtraffic.demo/inline/{creative_id}"
        execute(
            "UPDATE creatives SET vast_url = ?, measurement_config = ? WHERE id = ?",
            (vast_url, json.dumps(vendor_list), creative_id),
        )

    syntax = Syntax(xml, "xml", theme="monokai", line_numbers=True)
    console.print(syntax)
    console.print(f"\n[green]VAST 4.2 tag generated with vendors: {', '.join(vendor_list)}[/green]")


@cli.command("traffic")
@click.option("--creative-id", type=int, required=True, help="Creative ID")
@click.option("--dsp", multiple=True, default=["amazon", "thetradedesk"], help="DSP(s) to traffic to")
def cmd_traffic(creative_id, dsp):
    """Traffic a creative to one or more DSPs."""
    creative = fetch_one("SELECT * FROM creatives WHERE id = ?", (creative_id,))
    if creative is None:
        console.print(f"[red]Creative {creative_id} not found.[/red]")
        return

    if creative["approval_status"] not in ("approved", "trafficked", "active"):
        console.print(f"[yellow]Warning: Creative status is '{creative['approval_status']}'. "
                       f"Proceeding with simulated trafficking.[/yellow]")

    campaign = fetch_one("SELECT * FROM campaigns WHERE id = ?", (creative["campaign_id"],))
    campaign_name = campaign["name"] if campaign else "Demo Campaign"

    table = Table(title="Trafficking Results")
    table.add_column("DSP", style="cyan")
    table.add_column("Creative ID", style="green")
    table.add_column("Asset ID", style="green")
    table.add_column("Audit Status", style="yellow")
    table.add_column("Simulated", style="dim")

    for dsp_name in dsp:
        adapter = get_adapter(dsp_name)
        result = adapter.upload_creative(
            video_url=creative["video_url"] or "https://cdn.luma.example/demo.mp4",
            vast_url=creative["vast_url"] or f"https://vast.dreamtraffic.demo/inline/{creative_id}",
            duration_seconds=creative["duration_seconds"],
            width=creative["width"],
            height=creative["height"],
            placement_type=creative["placement_type"],
            campaign_name=campaign_name,
        )

        # Record trafficking
        execute(
            """INSERT INTO trafficking_records
               (creative_id, dsp, dsp_creative_id, dsp_asset_id, vast_url,
                audit_status, placement_type, request_payload, response_payload)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (creative_id, result.dsp, result.creative_id, result.asset_id,
             result.vast_url, result.audit_status, result.placement_type,
             json.dumps(result.request_payload), json.dumps(result.response_payload)),
        )

        table.add_row(
            result.dsp, result.creative_id, result.asset_id,
            result.audit_status, str(result._simulated),
        )

    console.print(table)


@cli.command("supply-chain")
@click.option("--creative-id", type=int, help="Creative ID for targeted analysis")
@click.option("--base-cpm", type=float, default=10.0, help="Base CPM for fee calculation")
def cmd_supply_chain(creative_id, base_cpm):
    """Analyze supply chain fee stacks across all DSP paths."""
    calc = FeeStackCalculator()
    router = BidswitchRouter()

    console.print("[bold]Supply Chain Fee Analysis[/bold]\n")
    console.print(f"Base CPM: ${base_cpm:.2f}")
    console.print(f"Luma Creative Gen CPM: ${calc.luma_cpm:.4f} (amortized)\n")

    comparison = calc.compare_dsps()
    for dsp, data in comparison.items():
        console.print(f"[bold cyan]{dsp.upper()}[/bold cyan]")
        console.print(f"  Paths: {data['path_count']}")
        console.print(f"  Avg DSP Fee: {data['avg_dsp_fee']}%")
        console.print(f"  Avg Total Supply Cost: {data['avg_total_supply_cost']}%")
        console.print(f"  Avg Publisher Net: {data['avg_publisher_net']}%")
        console.print(f"  Avg Measurement CPM: ${data['avg_measurement_cpm']}")
        console.print()

        for path in data["paths"]:
            console.print(f"    → {path['exchange'] or 'direct'} → {path['ssp']}: "
                          f"{path['total_cost_pct']}% cost, {path['publisher_net_pct']}% net")
        console.print()

    # Highlight ADSP advantage
    if "amazon" in comparison and "thetradedesk" in comparison:
        adsp = comparison["amazon"]
        ttd = comparison["thetradedesk"]
        savings = ttd["avg_total_supply_cost"] - adsp["avg_total_supply_cost"]
        console.print(f"[bold green]ADSP Advantage: {savings:.1f}% lower supply cost vs. TTD[/bold green]")
        console.print(f"On ${base_cpm:.2f} CPM, that's ${base_cpm * savings / 100:.2f} per thousand "
                       f"impressions freed up for Luma creative generation.\n")


@cli.command("approve")
@click.option("--creative-id", type=int, required=True)
@click.option("--action", type=click.Choice(["submit", "approve", "reject"]), required=True)
@click.option("--notes", default="", help="Review notes")
def cmd_approve(creative_id, action, notes):
    """Manage creative approval workflow."""
    workflow = ApprovalWorkflow()

    if action == "submit":
        result = workflow.submit_for_review(creative_id)
    elif action == "approve":
        result = workflow.approve(creative_id, notes=notes)
    elif action == "reject":
        result = workflow.request_revision(creative_id, notes=notes)

    console.print(f"[green]{result['from_status']} → {result['to_status']}[/green]")
    if result.get("notes"):
        console.print(f"  Notes: {result['notes']}")

    # Show timeline
    trail = workflow.get_audit_trail(creative_id)
    console.print(f"\n{format_timeline(trail)}")


@cli.command("status")
@click.option("--campaign-id", type=int, help="Show status for a specific campaign")
def cmd_status(campaign_id):
    """Show pipeline status for campaigns and creatives."""
    if campaign_id:
        campaigns = fetch_all("SELECT * FROM campaigns WHERE id = ?", (campaign_id,))
    else:
        campaigns = fetch_all("SELECT * FROM campaigns ORDER BY id")

    if not campaigns:
        console.print("[yellow]No campaigns found. Create one or run init-db.[/yellow]")
        return

    for c in campaigns:
        console.print(f"\n[bold]{c['name']}[/bold] (ID: {c['id']})")
        console.print(f"  Advertiser: {c['advertiser']}")
        console.print(f"  Flight: {c['flight_start']} → {c['flight_end']}")

        creatives = fetch_all(
            "SELECT * FROM creatives WHERE campaign_id = ? ORDER BY id",
            (c["id"],),
        )
        if creatives:
            table = Table()
            table.add_column("ID")
            table.add_column("Name")
            table.add_column("Status")
            table.add_column("Placement")
            table.add_column("Duration")
            table.add_column("DSPs Trafficked")

            for cr in creatives:
                trafficked = fetch_all(
                    "SELECT DISTINCT dsp FROM trafficking_records WHERE creative_id = ?",
                    (cr["id"],),
                )
                dsp_list = ", ".join(t["dsp"] for t in trafficked) or "—"
                table.add_row(
                    str(cr["id"]), cr["name"], cr["approval_status"],
                    cr["placement_type"], f"{cr['duration_seconds']}s", dsp_list,
                )
            console.print(table)


@cli.command("demo")
def cmd_demo():
    """Run a full demo pipeline with seed data (no Luma API calls)."""
    console.print("[bold]DreamTraffic Demo Pipeline[/bold]\n")

    # Init DB
    init_db()
    console.print("[green]1. Database initialized[/green]")

    # Create demo campaign
    cursor = execute(
        """INSERT INTO campaigns (name, advertiser, objective, audience, placements,
           budget, flight_start, flight_end, brief)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            "Luma AI CTV Launch",
            "Luma AI",
            "Brand awareness + consideration for Dream Machine",
            "Marketing decision makers, creative directors, agency planners",
            "olv,stv",
            250000.0,
            "2026-03-01",
            "2026-04-30",
            "Launch campaign for Luma AI Dream Machine targeting enterprise "
            "advertisers. Showcase AI-generated video quality for programmatic "
            "CTV and OLV placements.",
        ),
    )
    campaign_id = cursor.lastrowid
    console.print(f"[green]2. Campaign created (ID: {campaign_id})[/green]")

    # Create demo creatives
    for name, dur, placement in [("30s CTV Spot", 30, "stv"), ("15s Pre-roll", 15, "olv")]:
        execute(
            """INSERT INTO creatives (campaign_id, name, prompt, video_url,
               duration_seconds, placement_type, luma_generation_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                campaign_id, name,
                "Cinematic aerial shot of a futuristic city at golden hour, "
                "camera slowly descending through clouds to reveal gleaming towers, "
                "AI-generated holographic advertisements floating between buildings",
                "https://cdn.luma.example/demo-spot.mp4",
                dur, placement, "demo-gen-001",
            ),
        )
    console.print("[green]3. Creatives created (30s CTV + 15s Pre-roll)[/green]")

    # Generate VAST tags
    creatives = fetch_all("SELECT * FROM creatives WHERE campaign_id = ?", (campaign_id,))
    generator = VastGenerator()
    for cr in creatives:
        xml = generator.generate_inline(
            video_url=cr["video_url"],
            duration=f"00:00:{cr['duration_seconds']:02d}",
            title=cr["name"],
        )
        vast_url = f"https://vast.dreamtraffic.demo/inline/{cr['id']}"
        execute(
            "UPDATE creatives SET vast_url = ?, measurement_config = ? WHERE id = ?",
            (vast_url, json.dumps(["ias", "moat", "doubleverify"]), cr["id"]),
        )
    console.print("[green]4. VAST 4.2 tags generated with IAS + MOAT + DoubleVerify[/green]")

    # Approval workflow
    workflow = ApprovalWorkflow()
    for cr in creatives:
        workflow.submit_for_review(cr["id"])
        workflow.approve(cr["id"], notes="All DSP specs validated. OMID compliant.")
    console.print("[green]5. Creatives approved through compliance review[/green]")

    # Traffic to DSPs
    for cr in creatives:
        for dsp_name in ["amazon", "thetradedesk", "dv360"]:
            adapter = get_adapter(dsp_name)
            result = adapter.upload_creative(
                video_url=cr["video_url"],
                vast_url=cr["vast_url"],
                duration_seconds=cr["duration_seconds"],
                width=cr["width"],
                height=cr["height"],
                placement_type=cr["placement_type"],
                campaign_name="Luma AI CTV Launch",
            )
            execute(
                """INSERT INTO trafficking_records
                   (creative_id, dsp, dsp_creative_id, dsp_asset_id, vast_url,
                    audit_status, placement_type, request_payload, response_payload)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (cr["id"], result.dsp, result.creative_id, result.asset_id,
                 result.vast_url, result.audit_status, result.placement_type,
                 json.dumps(result.request_payload), json.dumps(result.response_payload)),
            )
        workflow.mark_trafficked(cr["id"])
    console.print("[green]6. Trafficked to Amazon DSP, TTD, and DV360[/green]")

    # Supply chain analysis
    console.print("[green]7. Supply chain analysis:[/green]")
    calc = FeeStackCalculator()
    comparison = calc.compare_dsps()
    for dsp, data in comparison.items():
        console.print(f"   {dsp}: {data['avg_total_supply_cost']}% avg supply cost, "
                       f"{data['avg_publisher_net']}% publisher net")

    if "amazon" in comparison and "thetradedesk" in comparison:
        savings = comparison["thetradedesk"]["avg_total_supply_cost"] - comparison["amazon"]["avg_total_supply_cost"]
        console.print(f"\n[bold green]   ADSP saves {savings:.1f}% vs TTD — "
                       f"margin freed for Luma creative generation[/bold green]")

    console.print("\n[bold]Demo complete. Run 'dreamtraffic status' to view pipeline.[/bold]")
