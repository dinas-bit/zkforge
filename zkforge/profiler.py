"""GPU profiling for ZK operations."""
import time
import logging
from collections import defaultdict

logger = logging.getLogger("zkforge.profiler")

class ZKProfiler:
    def __init__(self):
        self.timings = defaultdict(list)
    def record(self, op, ms):
        self.timings[op].append(ms)
    def summary(self):
        result = {}
        for op, times in self.timings.items():
            result[op] = {"count": len(times), "total_ms": sum(times),
                          "avg_ms": sum(times)/len(times), "max_ms": max(times)}
        return result
    def print_summary(self):
        s = self.summary()
        print("\n" + "=" * 50)
        print("ZKFORGE PROFILER")
        print("=" * 50)
        for op, d in s.items():
            print(f"  {op:20s} | {d['count']:5d} calls | avg {d['avg_ms']:.1f}ms | total {d['total_ms']:.0f}ms")
        print("=" * 50)
