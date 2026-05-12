"""Fiat-Shamir transcript for non-interactive proofs."""
import hashlib
import logging

logger = logging.getLogger("zkforge.transcript")

class Transcript:
    """Fiat-Shamir challenge generation."""
    def __init__(self, label: str):
        self.state = hashlib.sha256(label.encode()).digest()
    def append(self, label: str, data):
        h = hashlib.sha256()
        h.update(self.state)
        h.update(label.encode())
        h.update(str(data).encode())
        self.state = h.digest()
    def challenge(self, label: str) -> int:
        self.append(label, b"challenge")
        return int.from_bytes(self.state[:8], "big")
