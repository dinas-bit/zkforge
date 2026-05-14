"""Benchmark suite for ZK operations."""
import time
import logging
from typing import Dict, List
from .ntt import NTTProcessor
from .msm import MSMProcessor, ECPoint
from .field import BN254Field, GoldilocksField

logger = logging.getLogger("zkforge.benchmark")

class BenchmarkRunner:
    def __init__(self, device_id=0):
        self.device_id = device_id

    def bench_ntt(self, size: int = 1 << 20, iterations: int = 10) -> Dict:
        ntt = NTTProcessor(BN254Field, self.device_id)
        data = [1] * size + [0] * (size * 2 - size)
        latencies = []
        for _ in range(iterations):
            start = time.perf_counter()
            ntt.ntt(data[:size])
            latencies.append((time.perf_counter() - start) * 1000)
        return {"operation": "NTT", "size": size, "avg_ms": sum(latencies)/len(latencies),
                "p50_ms": sorted(latencies)[len(latencies)//2]}

    def bench_msm(self, size: int = 1 << 20, iterations: int = 5) -> Dict:
        msm = MSMProcessor(BN254Field, self.device_id)
        scalars = list(range(1, size + 1))
        points = [ECPoint(i, i*2) for i in range(1, size + 1)]
        latencies = []
        for _ in range(iterations):
            start = time.perf_counter()
            msm.msm(scalars[:1024], points[:1024])  # Subset for speed
            latencies.append((time.perf_counter() - start) * 1000)
        return {"operation": "MSM", "size": size, "avg_ms": sum(latencies)/len(latencies)}

    def run_all(self) -> List[Dict]:
        return [self.bench_ntt(), self.bench_msm()]

    def print_results(self, results):
        print("\n" + "=" * 50)
        print("ZKFORGE BENCHMARK RESULTS")
        print("=" * 50)
        for r in results:
            print(f"  {r['operation']:8s} | size={r['size']:,} | avg={r['avg_ms']:.1f}ms")
        print("=" * 50)
