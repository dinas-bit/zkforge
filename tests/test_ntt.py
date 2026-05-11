import pytest
from zkforge.field import GoldilocksField
from zkforge.ntt import NTTProcessor

class TestNTT:
    def test_ntt_inverse(self):
        ntt = NTTProcessor(GoldilocksField)
        a = [1, 2, 3, 4, 0, 0, 0, 0]
        a_ntt = ntt.ntt(a)
        a_back = ntt.ntt(a_ntt, inverse=True)
        assert a_back[:4] == [1, 2, 3, 4]

    def test_polynomial_mul(self):
        ntt = NTTProcessor(GoldilocksField)
        # (1 + 2x) * (3 + 4x) = 3 + 10x + 8x^2
        result = ntt.polynomial_mul([1, 2], [3, 4])
        assert result[0] == 3
