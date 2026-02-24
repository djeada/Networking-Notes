"""
OSI Model Simulator
====================
Simulates data passing through the 7 layers of the OSI (Open Systems
Interconnection) model. Demonstrates encapsulation (adding headers/trailers
as data moves down the stack) and decapsulation (stripping them as data
moves up the stack on the receiving side).

Each layer is represented by a class that wraps or unwraps a data unit,
mirroring how real network stacks operate.

Layers (top to bottom):
    7 - Application    : User data / HTTP headers
    6 - Presentation   : Encoding / encryption info
    5 - Session        : Session identifiers
    4 - Transport       : TCP/UDP port info, sequence numbers
    3 - Network         : IP addresses
    2 - Data Link       : MAC addresses, frame trailer (FCS)
    1 - Physical        : Bit-stream representation
"""

import textwrap


# ---------------------------------------------------------------------------
# Data‑unit container shared across layers
# ---------------------------------------------------------------------------
class DataUnit:
    """Represents the protocol data unit (PDU) at any layer."""

    def __init__(self, payload: str):
        self.headers: list[str] = []
        self.payload: str = payload
        self.trailers: list[str] = []

    def add_header(self, header: str) -> None:
        self.headers.insert(0, header)

    def add_trailer(self, trailer: str) -> None:
        self.trailers.append(trailer)

    def remove_header(self) -> str:
        return self.headers.pop(0) if self.headers else ""

    def remove_trailer(self) -> str:
        return self.trailers.pop() if self.trailers else ""

    def __str__(self) -> str:
        parts = self.headers + [self.payload] + self.trailers
        return " | ".join(parts)


# ---------------------------------------------------------------------------
# Layer base class
# ---------------------------------------------------------------------------
class OSILayer:
    """Abstract base for an OSI layer."""

    number: int = 0
    name: str = ""
    pdu_name: str = "Data"

    def encapsulate(self, data_unit: DataUnit) -> DataUnit:
        raise NotImplementedError

    def decapsulate(self, data_unit: DataUnit) -> DataUnit:
        raise NotImplementedError

    def _log(self, direction: str, detail: str) -> None:
        arrow = "▼" if direction == "down" else "▲"
        print(f"  {arrow} Layer {self.number} ({self.name:14s}) "
              f"[{self.pdu_name:8s}] {detail}")


# ---------------------------------------------------------------------------
# Concrete layers
# ---------------------------------------------------------------------------
class ApplicationLayer(OSILayer):
    number, name, pdu_name = 7, "Application", "Data"

    def encapsulate(self, data_unit: DataUnit) -> DataUnit:
        header = "APP-HDR(HTTP GET /index.html)"
        data_unit.add_header(header)
        self._log("down", f"Added header: {header}")
        return data_unit

    def decapsulate(self, data_unit: DataUnit) -> DataUnit:
        hdr = data_unit.remove_header()
        self._log("up", f"Removed header: {hdr}")
        return data_unit


class PresentationLayer(OSILayer):
    number, name, pdu_name = 6, "Presentation", "Data"

    def encapsulate(self, data_unit: DataUnit) -> DataUnit:
        header = "PRES-HDR(encoding=UTF-8)"
        data_unit.add_header(header)
        self._log("down", f"Added header: {header}")
        return data_unit

    def decapsulate(self, data_unit: DataUnit) -> DataUnit:
        hdr = data_unit.remove_header()
        self._log("up", f"Removed header: {hdr}")
        return data_unit


class SessionLayer(OSILayer):
    number, name, pdu_name = 5, "Session", "Data"

    def encapsulate(self, data_unit: DataUnit) -> DataUnit:
        header = "SESS-HDR(id=0xA1B2)"
        data_unit.add_header(header)
        self._log("down", f"Added header: {header}")
        return data_unit

    def decapsulate(self, data_unit: DataUnit) -> DataUnit:
        hdr = data_unit.remove_header()
        self._log("up", f"Removed header: {hdr}")
        return data_unit


class TransportLayer(OSILayer):
    number, name, pdu_name = 4, "Transport", "Segment"

    def encapsulate(self, data_unit: DataUnit) -> DataUnit:
        header = "TCP-HDR(src=49152,dst=80,seq=1)"
        data_unit.add_header(header)
        self._log("down", f"Added header: {header}")
        return data_unit

    def decapsulate(self, data_unit: DataUnit) -> DataUnit:
        hdr = data_unit.remove_header()
        self._log("up", f"Removed header: {hdr}")
        return data_unit


class NetworkLayer(OSILayer):
    number, name, pdu_name = 3, "Network", "Packet"

    def encapsulate(self, data_unit: DataUnit) -> DataUnit:
        header = "IP-HDR(src=192.168.1.10,dst=93.184.216.34)"
        data_unit.add_header(header)
        self._log("down", f"Added header: {header}")
        return data_unit

    def decapsulate(self, data_unit: DataUnit) -> DataUnit:
        hdr = data_unit.remove_header()
        self._log("up", f"Removed header: {hdr}")
        return data_unit


class DataLinkLayer(OSILayer):
    number, name, pdu_name = 2, "Data Link", "Frame"

    def encapsulate(self, data_unit: DataUnit) -> DataUnit:
        header = "ETH-HDR(src=AA:BB:CC:DD:EE:01,dst=AA:BB:CC:DD:EE:02)"
        trailer = "ETH-FCS(0x1A2B3C4D)"
        data_unit.add_header(header)
        data_unit.add_trailer(trailer)
        self._log("down", f"Added header: {header}")
        self._log("down", f"Added trailer: {trailer}")
        return data_unit

    def decapsulate(self, data_unit: DataUnit) -> DataUnit:
        trl = data_unit.remove_trailer()
        hdr = data_unit.remove_header()
        self._log("up", f"Removed trailer: {trl}")
        self._log("up", f"Removed header: {hdr}")
        return data_unit


class PhysicalLayer(OSILayer):
    number, name, pdu_name = 1, "Physical", "Bits"

    def encapsulate(self, data_unit: DataUnit) -> DataUnit:
        self._log("down", "Converted frame to bit-stream for transmission")
        return data_unit

    def decapsulate(self, data_unit: DataUnit) -> DataUnit:
        self._log("up", "Received bit-stream and reconstructed frame")
        return data_unit


# ---------------------------------------------------------------------------
# Stack coordinator
# ---------------------------------------------------------------------------
# Layer ordering from top (Application) to bottom (Physical)
LAYERS = [
    ApplicationLayer(),
    PresentationLayer(),
    SessionLayer(),
    TransportLayer(),
    NetworkLayer(),
    DataLinkLayer(),
    PhysicalLayer(),
]


def send(message: str) -> DataUnit:
    """Simulate the sending side: encapsulate through all layers."""
    print("=" * 70)
    print("SENDER — Encapsulation (travelling DOWN the OSI stack)")
    print("=" * 70)
    du = DataUnit(payload=message)
    print(f"  Original data: {message!r}\n")
    for layer in LAYERS:
        du = layer.encapsulate(du)
    print(f"\n  On the wire: {du}\n")
    return du


def receive(data_unit: DataUnit) -> str:
    """Simulate the receiving side: decapsulate through all layers."""
    print("=" * 70)
    print("RECEIVER — Decapsulation (travelling UP the OSI stack)")
    print("=" * 70)
    print(f"  Received from wire: {data_unit}\n")
    for layer in reversed(LAYERS):
        data_unit = layer.decapsulate(data_unit)
    print(f"\n  Extracted data: {data_unit.payload!r}")
    return data_unit.payload


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    message = "Hello, Network World!"
    wire_data = send(message)
    print()
    received = receive(wire_data)
    print("\n" + "=" * 70)
    print(f"Message integrity check: {'PASS' if received == message else 'FAIL'}")
    print("=" * 70)
