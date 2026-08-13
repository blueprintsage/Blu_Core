"""Terminal host adapter.

The only Phase-1 host binding. Terminal mechanics only: it does not decide
security, routing, continuity, or truth.
"""

from __future__ import annotations

import sys
import uuid
from typing import Callable, TextIO

from blu_runtime.adapters.host.base import HostAdapter
from blu_runtime.contracts.models import (
    BLOCK,
    INVALID,
    PASS,
    UNAVAILABLE,
    HostInput,
    RawHostEvent,
    TerminalPacket,
)

PROMPT = "you> "
REPLY_PREFIX = "blu> "

#: Safe, non-echoing terminal text per terminal status. A protected ingress
#: match must never be echoed or characterized.
STATUS_TEXT = {
    BLOCK: "I can't work with that here.",
    UNAVAILABLE: "That isn't available in this runtime right now.",
    INVALID: "That input wasn't usable.",
}


class TerminalHostAdapter(HostAdapter):
    """One terminal input in, one terminal packet out, one reply rendered."""

    host = "terminal"

    def __init__(
        self,
        stream_in: TextIO | None = None,
        stream_out: TextIO | None = None,
        request_id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._in = stream_in or sys.stdin
        self._out = stream_out or sys.stdout
        self._request_id_factory = request_id_factory or (lambda: uuid.uuid4().hex)

    def receive(self) -> RawHostEvent | None:
        self._out.write(PROMPT)
        self._out.flush()
        line = self._in.readline()
        # End of stream is an out-of-band host mechanic, not user text.
        if not line:
            return None
        # B-06: no in-band command is privileged. Slash-prefixed text becomes an
        # ordinary host event, runs the full security and routing path, and
        # terminates as an unsupported route like any other slash command.
        text = line.rstrip("\n").rstrip("\r")
        return RawHostEvent(host=self.host, event_id=self._request_id_factory(), text=text)

    def submit(self, event: RawHostEvent) -> HostInput:
        return HostInput(host=self.host, request_id=event.event_id, text=event.text)

    def render(self, packet: TerminalPacket) -> str:
        """Render exactly one authorized terminal packet."""
        if packet.status == PASS and packet.public_output is not None:
            body = packet.public_output
        else:
            body = STATUS_TEXT.get(packet.status, "That isn't available right now.")
        line = f"{REPLY_PREFIX}{body}"
        self._out.write(line + "\n")
        self._out.flush()
        return line
