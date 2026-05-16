# ZKForge Architecture

## Pipeline

```
Circuit (R1CS) → Setup → Witness → NTT → MSM → Proof → Verify
```

## GPU Operations

| Module | Operation | Kernel |
|--------|-----------|--------|
| NTT | Polynomial NTT | ntt_butterfly.hip |
| MSM | Multi-scalar mul | msm_bucket_accumulate.hip |
| Field | Modular arithmetic | field_ops.hip |

## Proof Systems

| System | Trusted Setup | Proof Size | Verify Time |
|--------|--------------|-----------|-------------|
| Groth16 | Yes | 3 elements | ~2ms |
| PLONK | Universal | 7 elements | ~5ms |
| STARK | No | O(log^2 n) | ~20ms |
