"""Database layer — SQLite with dataclass models."""

from dreamtraffic.db.engine import get_connection, execute, fetch_one, fetch_all
from dreamtraffic.db.models import (
    Campaign,
    Creative,
    ApprovalEvent,
    TraffickingRecord,
    SupplyPath,
    DSPSpec,
)

__all__ = [
    "get_connection",
    "execute",
    "fetch_one",
    "fetch_all",
    "Campaign",
    "Creative",
    "ApprovalEvent",
    "TraffickingRecord",
    "SupplyPath",
    "DSPSpec",
]
