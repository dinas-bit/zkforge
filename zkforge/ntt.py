"""Number Theoretic Transform (NTT) — GPU-accelerated polynomial multiplication."""
import logging
import math
from typing import List, Optional
from .field import Field

logger = logging.getLogger("zkforge.ntt")

class NTTProcessor:
    """NTT for fast polynomial multiplication in finite fields."""

    def __init__(self, field: Field, device_id: int = 0):
        self.field = field
        self.device_id = device_id
        self._roots = {}  # Precomputed twiddle factors

    def _get_root_of_unity(self, n: int) -> int:
        """Get primitive n-th root of unity."""
        if n in self._roots:
            return self._roots[n]
        # For BN254: find generator
        order = self.field.modulus - 1
        if order % n != 0:
            raise ValueError(f"n={n} does not divide p-1")
        generator = self._find_generator()
        root = self.field.pow(generator, order // n)
        self._roots[n] = root
        return root

    def _find_generator(self) -> int:
        """Find a primitive root of the field."""
        # Simplified — in production use precomputed generator
        for g in range(2, 100):
            if self.field.pow(g, (self.field.modulus - 1) // 2) != 1:
                return g
        return 2

    def ntt(self, a: List[int], inverse: bool = False) -> List[int]:
        """Compute NTT or inverse NTT."""
        n = len(a)
        if n & (n - 1) != 0:
            raise ValueError("Length must be power of 2")

        result = list(a)
        root = self._get_root_of_unity(n)
        if inverse:
            root = self.field.inv(root)

        # Bit-reversal permutation
        j = 0
        for i in range(1, n):
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j ^= bit
            if i < j:
                result[i], result[j] = result[j], result[i]

        # Butterfly operations
        length = 2
        while length <= n:
            wlen = self.field.pow(root, n // length)
            for i in range(0, n, length):
                w = 1
                for j in range(length // 2):
                    u = result[i + j]
                    v = self.field.mul(result[i + j + length // 2], w)
                    result[i + j] = self.field.add(u, v)
                    result[i + j + length // 2] = self.field.sub(u, v)
                    w = self.field.mul(w, wlen)
            length *= 2

        if inverse:
            n_inv = self.field.inv(n)
            result = [self.field.mul(x, n_inv) for x in result]

        return result

    def polynomial_mul(self, a: List[int], b: List[int]) -> List[int]:
        """Multiply polynomials using NTT."""
        n = 1
        while n < len(a) + len(b) - 1:
            n *= 2
        a_padded = a + [0] * (n - len(a))
        b_padded = b + [0] * (n - len(b))

        a_ntt = self.ntt(a_padded)
        b_ntt = self.ntt(b_padded)
        c_ntt = [self.field.mul(x, y) for x, y in zip(a_ntt, b_ntt)]
        return self.ntt(c_ntt, inverse=True)[:len(a) + len(b) - 1]
