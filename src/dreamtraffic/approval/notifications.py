"""Rich CLI status formatting for approval workflow."""

from __future__ import annotations

from dreamtraffic.db.models import ApprovalStatus

STATUS_ICONS = {
    ApprovalStatus.DRAFT.value: "[dim]DRAFT[/dim]",
    ApprovalStatus.PENDING_REVIEW.value: "[yellow]PENDING REVIEW[/yellow]",
    ApprovalStatus.REVISION_REQUESTED.value: "[red]REVISION REQUESTED[/red]",
    ApprovalStatus.APPROVED.value: "[green]APPROVED[/green]",
    ApprovalStatus.TRAFFICKED.value: "[blue]TRAFFICKED[/blue]",
    ApprovalStatus.ACTIVE.value: "[bold green]ACTIVE[/bold green]",
    ApprovalStatus.PAUSED.value: "[yellow]PAUSED[/yellow]",
    ApprovalStatus.ARCHIVED.value: "[dim]ARCHIVED[/dim]",
}


def format_status(status: str) -> str:
    """Format a status string with Rich markup."""
    return STATUS_ICONS.get(status, status)


def format_timeline(audit_trail: list[dict]) -> str:
    """Format an audit trail as a timeline string."""
    if not audit_trail:
        return "No approval events recorded."

    lines = ["Approval Timeline:", ""]
    for event in audit_trail:
        from_s = format_status(event["from_status"])
        to_s = format_status(event["to_status"])
        reviewer = event.get("reviewer", "system")
        notes = event.get("notes", "")
        ts = event.get("created_at", "")

        lines.append(f"  {from_s} -> {to_s}")
        lines.append(f"    Reviewer: {reviewer}")
        if notes:
            lines.append(f"    Notes: {notes}")
        lines.append(f"    Time: {ts}")
        lines.append("")

    return "\n".join(lines)
