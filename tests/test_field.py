import pytest
from zkforge.field import BN254Field, GoldilocksField

class TestField:
    def test_add(self):
        assert BN254Field.add(5, 3) == 8
    def test_mul(self):
        assert BN254Field.mul(5, 3) == 15
    def test_inv(self):
        a = 42
        assert BN254Field.mul(a, BN254Field.inv(a)) == 1
    def test_neg(self):
        assert BN254Field.add(5, BN254Field.neg(5)) == 0
