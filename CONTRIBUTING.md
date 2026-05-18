# Contributing to ZKForge

## Adding a New Proof System

1. Create `zkforge/prover/your_system.py`
2. Implement `prove()` and `verify()` methods
3. Add to CLI choices
4. Write tests

## Adding a New Curve

1. Define field in `zkforge/field.py`
2. Add curve parameters
3. Test NTT/MSM with new field
