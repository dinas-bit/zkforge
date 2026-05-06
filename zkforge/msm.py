"""Multi-Scalar Multiplication (MSM) — GPU-accelerated elliptic curve operations."""
import logging
from typing import List, Tuple
from .field import Field

logger = logging.getLogger("zkforge.msm")

class ECPoint:
    """Elliptic curve point (affine coordinates)."""
    def __init__(self, x: int, y: int, infinity: bool = False):
        self.x = x
        self.y = y
        self.infinity = infinity

    def __eq__(self, other):
        if self.infinity and other.infinity: return True
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        if self.infinity: return "Point(INFINITY)"
        return f"Point({self.x}, {self.y})"


class MSMProcessor:
    """Multi-Scalar Multiplication: compute sum(s_i * P_i)."""

    def __init__(self, field: Field, device_id: int = 0):
        self.field = field
        self.device_id = device_id

    def msm(self, scalars: List[int], points: List[ECPoint]) -> ECPoint:
        """Compute sum(s_i * P_i) using Pippenger's algorithm."""
        if len(scalars) != len(points):
            raise ValueError("Scalars and points must have same length")

        n = len(scalars)
        if n == 0:
            return ECPoint(0, 0, infinity=True)

        # Window size for Pippenger
        c = max(1, (n * 2).bit_length() // 2)
        num_windows = (self.field.bits + c - 1) // c

        result = ECPoint(0, 0, infinity=True)

        for window in range(num_windows - 1, -1, -1):
            # Accumulate within window
            buckets = [ECPoint(0, 0, infinity=True) for _ in range(1 << c)]
            for i in range(n):
                bucket_idx = (scalars[i] >> (window * c)) & ((1 << c) - 1)
                if bucket_idx > 0:
                    buckets[bucket_idx] = self._ec_add(buckets[bucket_idx], points[i])

            # Sum buckets
            bucket_sum = ECPoint(0, 0, infinity=True)
            running = ECPoint(0, 0, infinity=True)
            for j in range((1 << c) - 1, 0, -1):
                running = self._ec_add(running, buckets[j])
                bucket_sum = self._ec_add(bucket_sum, running)

            # Shift result
            for _ in range(c):
                result = self._ec_double(result)
            result = self._ec_add(result, bucket_sum)

        return result

    def _ec_add(self, p: ECPoint, q: ECPoint) -> ECPoint:
        if p.infinity: return q
        if q.infinity: return p
        if p.x == q.x and p.y != q.y:
            return ECPoint(0, 0, infinity=True)
        if p.x == q.x:
            return self._ec_double(p)
        lam = self.field.mul(self.field.sub(q.y, p.y), self.field.inv(self.field.sub(q.x, p.x)))
        x = self.field.sub(self.field.sub(self.field.mul(lam, lam), p.x), q.x)
        y = self.field.sub(self.field.mul(lam, self.field.sub(p.x, x)), p.y)
        return ECPoint(x, y)

    def _ec_double(self, p: ECPoint) -> ECPoint:
        if p.infinity: return p
        # y^2 = x^3 + 3 (BN254 curve)
        lam = self.field.mul(
            self.field.add(self.field.mul(3, self.field.mul(p.x, p.x)), 3),
            self.field.inv(self.field.mul(2, p.y))
        )
        x = self.field.sub(self.field.mul(lam, lam), self.field.mul(2, p.x))
        y = self.field.sub(self.field.mul(lam, self.field.sub(p.x, x)), p.y)
        return ECPoint(x, y)
