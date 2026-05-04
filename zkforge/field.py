"""Finite field arithmetic for ZK proof systems."""
import logging
from typing import Union

logger = logging.getLogger("zkforge.field")

class Field:
    """Generic prime field arithmetic."""

    def __init__(self, modulus: int, name: str = "custom"):
        self.modulus = modulus
        self.name = name
        self.bits = modulus.bit_length()

    def add(self, a: int, b: int) -> int:
        return (a + b) % self.modulus

    def sub(self, a: int, b: int) -> int:
        return (a - b) % self.modulus

    def mul(self, a: int, b: int) -> int:
        return (a * b) % self.modulus

    def inv(self, a: int) -> int:
        return pow(a, self.modulus - 2, self.modulus)  # Fermat's little theorem

    def pow(self, base: int, exp: int) -> int:
        return pow(base, exp, self.modulus)

    def neg(self, a: int) -> int:
        return (self.modulus - a) % self.modulus

    def sqrt(self, a: int) -> int:
        """Tonelli-Shanks square root."""
        if pow(a, (self.modulus - 1) // 2, self.modulus) != 1:
            raise ValueError("Not a quadratic residue")
        # Simplified for p ≡ 3 (mod 4)
        if self.modulus % 4 == 3:
            return pow(a, (self.modulus + 1) // 4, self.modulus)
        raise NotImplementedError("Tonelli-Shanks for general case")

    def __repr__(self):
        return f"Field({self.name}, {self.bits}-bit)"


# Standard fields used in ZK proofs
BN254Field = Field(
    modulus=21888242871839275222246405745257275088548364400416034343698204186575808495617,
    name="BN254"
)

BLS12Field = Field(
    modulus=4002409555221667393417789825735904156556882819939007885332058136124031650490837864442687629129015664037894272559787,
    name="BLS12-381"
)

GoldilocksField = Field(
    modulus=18446744069414584321,
    name="Goldilocks"
)
