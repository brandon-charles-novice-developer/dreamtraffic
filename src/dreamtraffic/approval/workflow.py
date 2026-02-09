"""Approval state machine with transition validation and audit trail."""

from __future__ import annotations

from dreamtraffic.db.models import ApprovalStatus
from dreamtraffic.db.engine import execute, fetch_one, fetch_all

# Valid state transitions
TRANSITIONS: dict[str, list[str]] = {
    ApprovalStatus.DRAFT.value: [ApprovalStatus.PENDING_REVIEW.value],
    ApprovalStatus.PENDING_REVIEW.value: [
        ApprovalStatus.APPROVED.value,
        ApprovalStatus.REVISION_REQUESTED.value,
    ],
    ApprovalStatus.REVISION_REQUESTED.value: [ApprovalStatus.PENDING_REVIEW.value],
    ApprovalStatus.APPROVED.value: [ApprovalStatus.TRAFFICKED.value],
    ApprovalStatus.TRAFFICKED.value: [ApprovalStatus.ACTIVE.value, ApprovalStatus.PAUSED.value],
    ApprovalStatus.ACTIVE.value: [ApprovalStatus.PAUSED.value, ApprovalStatus.ARCHIVED.value],
    ApprovalStatus.PAUSED.value: [ApprovalStatus.ACTIVE.value, ApprovalStatus.ARCHIVED.value],
    ApprovalStatus.ARCHIVED.value: [],
}


class ApprovalWorkflow:
    """State machine for creative approval with audit trail."""

    def get_status(self, creative_id: int) -> str:
        """Get current approval status for a creative."""
        row = fetch_one("SELECT approval_status FROM creatives WHERE id = ?", (creative_id,))
        if row is None:
            raise ValueError(f"Creative {creative_id} not found")
        return row["approval_status"]

    def get_valid_transitions(self, creative_id: int) -> list[str]:
        """Get valid next states for a creative."""
        current = self.get_status(creative_id)
        return TRANSITIONS.get(current, [])

    def transition(
        self,
        creative_id: int,
        to_status: str,
        *,
        reviewer: str = "system",
        notes: str = "",
    ) -> dict:
        """Transition a creative to a new approval status.

        Returns dict with from_status, to_status, and success flag.
        Raises ValueError if transition is invalid.
        """
        from_status = self.get_status(creative_id)
        valid = TRANSITIONS.get(from_status, [])

        if to_status not in valid:
            raise ValueError(
                f"Invalid transition: {from_status} → {to_status}. "
                f"Valid transitions: {valid}"
            )

        # Update creative status
        execute(
            "UPDATE creatives SET approval_status = ? WHERE id = ?",
            (to_status, creative_id),
        )

        # Record audit event
        execute(
            """INSERT INTO approval_events (creative_id, from_status, to_status, reviewer, notes)
               VALUES (?, ?, ?, ?, ?)""",
            (creative_id, from_status, to_status, reviewer, notes),
        )

        return {
            "creative_id": creative_id,
            "from_status": from_status,
            "to_status": to_status,
            "reviewer": reviewer,
            "notes": notes,
        }

    def submit_for_review(self, creative_id: int, *, reviewer: str = "system") -> dict:
        """Submit a draft creative for review."""
        return self.transition(
            creative_id,
            ApprovalStatus.PENDING_REVIEW.value,
            reviewer=reviewer,
            notes="Submitted for compliance review",
        )

    def approve(self, creative_id: int, *, reviewer: str = "compliance_reviewer", notes: str = "") -> dict:
        """Approve a creative."""
        return self.transition(
            creative_id,
            ApprovalStatus.APPROVED.value,
            reviewer=reviewer,
            notes=notes or "Creative approved — meets all DSP specifications",
        )

    def request_revision(self, creative_id: int, *, reviewer: str = "compliance_reviewer", notes: str = "") -> dict:
        """Request revision on a creative."""
        return self.transition(
            creative_id,
            ApprovalStatus.REVISION_REQUESTED.value,
            reviewer=reviewer,
            notes=notes or "Revision needed",
        )

    def mark_trafficked(self, creative_id: int) -> dict:
        """Mark a creative as trafficked to DSPs."""
        return self.transition(
            creative_id,
            ApprovalStatus.TRAFFICKED.value,
            reviewer="trafficking_manager",
            notes="Creative uploaded to all target DSPs",
        )

    def activate(self, creative_id: int) -> dict:
        """Mark a creative as active (serving impressions)."""
        return self.transition(
            creative_id,
            ApprovalStatus.ACTIVE.value,
            reviewer="system",
            notes="DSP audits passed — creative now serving",
        )

    def get_audit_trail(self, creative_id: int) -> list[dict]:
        """Get the full audit trail for a creative."""
        return fetch_all(
            """SELECT * FROM approval_events
               WHERE creative_id = ?
               ORDER BY created_at ASC""",
            (creative_id,),
        )
