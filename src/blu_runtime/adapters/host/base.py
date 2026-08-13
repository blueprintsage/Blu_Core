"""Generic Host Adapter Boundary.

An adapter may translate host mechanics. It may not redefine Blu behavior,
bypass security, invent continuity, invent authorization, or treat provider
output as already validated. It prints only a completed, authorized terminal
packet.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from blu_runtime.contracts.models import HostInput, RawHostEvent, TerminalPacket


class HostAdapter(ABC):
    """One host binding."""

    host: str

    @abstractmethod
    def receive(self) -> RawHostEvent | None:
        """Return one raw host event, or None when the host session ends."""

    @abstractmethod
    def submit(self, event: RawHostEvent) -> HostInput:
        """Normalize a raw host event for the deterministic core."""

    @abstractmethod
    def render(self, packet: TerminalPacket) -> str:
        """Render exactly one user-visible response from one terminal packet."""
