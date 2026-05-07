"""Rank-1 Constraint System (R1CS) for arithmetic circuits."""
import logging
from typing import List, Dict
from dataclasses import dataclass

logger = logging.getLogger("zkforge.circuits.r1cs")

@dataclass
class Constraint:
    """Single R1CS constraint: A * B = C."""
    a: Dict[int, int]  # variable_index -> coefficient
    b: Dict[int, int]
    c: Dict[int, int]

class R1CS:
    """Rank-1 Constraint System."""

    def __init__(self, num_variables: int, num_public: int = 1):
        self.num_variables = num_variables
        self.num_public = num_public
        self.constraints: List[Constraint] = []

    def add_constraint(self, a: Dict[int, int], b: Dict[int, int], c: Dict[int, int]):
        self.constraints.append(Constraint(a=a, b=b, c=c))

    def check_witness(self, witness: List[int], field) -> bool:
        """Verify that a witness satisfies all constraints."""
        for i, constraint in enumerate(self.constraints):
            a_val = sum(witness[idx] * coeff for idx, coeff in constraint.a.items()) % field.modulus
            b_val = sum(witness[idx] * coeff for idx, coeff in constraint.b.items()) % field.modulus
            c_val = sum(witness[idx] * coeff for idx, coeff in constraint.c.items()) % field.modulus
            if field.mul(a_val, b_val) != c_val:
                logger.error(f"Constraint {i} failed: {a_val} * {b_val} != {c_val}")
                return False
        return True

    def size(self) -> int:
        return len(self.constraints)

    @staticmethod
    def from_multiplication_gate(x: int, y: int, z: int) -> "R1CS":
        """Create R1CS for single multiplication gate: x * y = z."""
        r1cs = R1CS(num_variables=4, num_public=1)
        r1cs.add_constraint(
            a={x: 1}, b={y: 1}, c={z: 1}
        )
        return r1cs
