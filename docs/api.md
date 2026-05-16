# ZKForge API

## NTT
```python
from zkforge import NTTProcessor, BN254Field
ntt = NTTProcessor(BN254Field)
result = ntt.ntt([1, 2, 3, 4, 0, 0, 0, 0])
```

## MSM
```python
from zkforge import MSMProcessor, ECPoint
msm = MSMProcessor(BN254Field)
result = msm.msm([1, 2, 3], [P1, P2, P3])
```
