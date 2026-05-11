"""Polynomial commitment schemes — KZG, FRI."""
import hashlib
import logging
from typing import List
from .field import Field
from .msm import MSMProcessor, ECPoint

logger = logging.getLogger("zkforge.commitment")

class KZGCommitment:
    """Kate-Zaverucha-Goldberg polynomial commitment."""
    def __init__(self, field, device_id=0):
        self.field = field
        self.msm = MSMProcessor(field, device_id)
    def commit(self, coeffs, srs):
        points = [srs[i] for i in range(len(coeffs))]
        return self.msm.msm(coeffs, points)
    def open(self, coeffs, point, srs):
        quotient = self._divide_polynomial(coeffs, point)
        return self.commit(quotient, srs)
    def _divide_polynomial(self, coeffs, point):
        n = len(coeffs)
        quotient = [0] * (n - 1)
        remainder = coeffs[-1]
        for i in range(n - 2, -1, -1):
            quotient[i] = remainder
            remainder = coeffs[i] + self.field.mul(remainder, point)
        return quotient

class FRICommitment:
    """FRI polynomial commitment for STARKs."""
    def __init__(self, field, device_id=0):
        self.field = field
    def commit(self, evaluations):
        return hashlib.sha256(str(evaluations).encode()).hexdigest()
    def query(self, evaluations, index):
        return evaluations[index]
