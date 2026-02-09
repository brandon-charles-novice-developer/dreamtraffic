"""DSP adapters — Amazon DSP, TTD, DV360, challengers."""

from dreamtraffic.dsp.base import DSPAdapter
from dreamtraffic.dsp.amazon import AmazonDSPAdapter
from dreamtraffic.dsp.thetradedesk import TTDAdapter
from dreamtraffic.dsp.dv360 import DV360Adapter
from dreamtraffic.dsp.challenger import StackAdaptAdapter, AdelphicAdapter

_ADAPTERS: dict[str, type[DSPAdapter]] = {
    "amazon": AmazonDSPAdapter,
    "thetradedesk": TTDAdapter,
    "dv360": DV360Adapter,
    "stackadapt": StackAdaptAdapter,
    "adelphic": AdelphicAdapter,
}


def get_adapter(dsp: str) -> DSPAdapter:
    """Factory: get a DSP adapter by name."""
    cls = _ADAPTERS.get(dsp)
    if cls is None:
        raise ValueError(f"Unknown DSP: {dsp}. Available: {list(_ADAPTERS.keys())}")
    return cls()


__all__ = [
    "DSPAdapter",
    "get_adapter",
    "AmazonDSPAdapter",
    "TTDAdapter",
    "DV360Adapter",
    "StackAdaptAdapter",
    "AdelphicAdapter",
]
