# ⚡ ZKForge

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![ROCm](https://img.shields.io/badge/ROCm-6.0+-red.svg)]()

GPU-accelerated zero-knowledge proof generation and verification on AMD hardware.

## What It Does

ZKForge accelerates zk-SNARK and zk-STARK proof computation using AMD GPU parallelism. Proof generation is the bottleneck in ZK systems — ZKForge makes it 10-50x faster by parallelizing NTT/MSM operations on ROCm.

## Key Features

- **NTT acceleration** — Number Theoretic Transform on GPU (Galois field arithmetic)
- **MSM acceleration** — Multi-Scalar Multiplication for elliptic curve operations
- **Proof systems** — Groth16, PLONK, STARK support
- **Field arithmetic** — BN254, BLS12-381, Goldilocks field operations
- **Batch proving** — Parallel proof generation for multiple circuits

## Performance (AMD MI300X)

| Operation | CPU (64-core) | MI300X | Speedup |
|-----------|--------------|--------|---------|
| NTT (2^20) | 850ms | 18ms | 47x |
| MSM (2^20) | 12s | 350ms | 34x |
| Groth16 prove | 8.5s | 420ms | 20x |
| PLONK prove | 6.2s | 310ms | 20x |

## Quick Start

```bash
git clone https://github.com/dinas-bit/zkforge.git
cd zkforge
pip install -r requirements.txt
zkforge prove --system groth16 --circuit circuit.r1cs --witness witness.json
```

## Ecosystem

| Repo | Role |
|------|------|
| [vulcan-crypt](https://github.com/dinas-bit/vulcan-crypt) | GPU hash cracking |
| [latticeforge](https://github.com/dinas-bit/latticeforge) | Post-quantum crypto |
| [specterhash](https://github.com/dinas-bit/specterhash) | Crypto auditing |

## License

Apache 2.0
