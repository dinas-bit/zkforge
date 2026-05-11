import pytest
from zkforge.field import BN254Field
from zkforge.msm import MSMProcessor, ECPoint

class TestMSM:
    def test_msm_single(self):
        msm = MSMProcessor(BN254Field)
        result = msm.msm([1], [ECPoint(1, 2)])
        assert result.x == 1

    def test_msm_zero(self):
        msm = MSMProcessor(BN254Field)
        result = msm.msm([], [])
        assert result.infinity
