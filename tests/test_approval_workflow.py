"""Tests for the approval state machine and audit trail."""

import pytest

from dreamtraffic.approval.workflow import ApprovalWorkflow, TRANSITIONS
from dreamtraffic.db.engine import fetch_one


class TestApprovalWorkflow:
    def setup_method(self):
        self.workflow = ApprovalWorkflow()

    def test_initial_status_is_draft(self, test_db):
        status = self.workflow.get_status(1)
        assert status == "draft"

    def test_submit_for_review(self, test_db):
        result = self.workflow.submit_for_review(1)
        assert result["from_status"] == "draft"
        assert result["to_status"] == "pending_review"
        assert self.workflow.get_status(1) == "pending_review"

    def test_approve_after_review(self, test_db):
        self.workflow.submit_for_review(1)
        result = self.workflow.approve(1, notes="Looks good")
        assert result["to_status"] == "approved"
        assert result["notes"] == "Looks good"

    def test_request_revision(self, test_db):
        self.workflow.submit_for_review(1)
        result = self.workflow.request_revision(1, notes="Fix duration")
        assert result["to_status"] == "revision_requested"

    def test_resubmit_after_revision(self, test_db):
        self.workflow.submit_for_review(1)
        self.workflow.request_revision(1, notes="Fix it")
        result = self.workflow.submit_for_review(1)
        assert result["to_status"] == "pending_review"

    def test_invalid_transition_raises(self, test_db):
        with pytest.raises(ValueError, match="Invalid transition"):
            self.workflow.approve(1)  # Can't approve from draft

    def test_mark_trafficked(self, test_db):
        self.workflow.submit_for_review(1)
        self.workflow.approve(1)
        result = self.workflow.mark_trafficked(1)
        assert result["to_status"] == "trafficked"

    def test_activate(self, test_db):
        self.workflow.submit_for_review(1)
        self.workflow.approve(1)
        self.workflow.mark_trafficked(1)
        result = self.workflow.activate(1)
        assert result["to_status"] == "active"

    def test_audit_trail(self, test_db):
        self.workflow.submit_for_review(1)
        self.workflow.approve(1, notes="Approved")
        trail = self.workflow.get_audit_trail(1)
        assert len(trail) == 2
        assert trail[0]["from_status"] == "draft"
        assert trail[1]["to_status"] == "approved"

    def test_valid_transitions(self, test_db):
        valid = self.workflow.get_valid_transitions(1)
        assert valid == ["pending_review"]

    def test_nonexistent_creative_raises(self, test_db):
        with pytest.raises(ValueError, match="not found"):
            self.workflow.get_status(999)

    def test_full_lifecycle(self, test_db):
        """Test the complete happy path: draft → active."""
        self.workflow.submit_for_review(1)
        self.workflow.approve(1)
        self.workflow.mark_trafficked(1)
        self.workflow.activate(1)
        assert self.workflow.get_status(1) == "active"

        trail = self.workflow.get_audit_trail(1)
        assert len(trail) == 4
        statuses = [e["to_status"] for e in trail]
        assert statuses == ["pending_review", "approved", "trafficked", "active"]
