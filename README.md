# ⚡ ZKForge

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![ROCm](https://img.shields.io/badge/ROCm-6.0+-red.svg)]()
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)]()

GPU-accelerated zero-knowledge proof generation and verification on AMD hardware.

## Performance (MI300X)

| Operation | CPU | MI300X | Speedup |
|-----------|-----|--------|---------|
| NTT (2^20) | 850ms | 18ms | 47x |
| MSM (2^20) | 12s | 350ms | 34x |
| Groth16 | 8.5s | 420ms | 20x |

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
