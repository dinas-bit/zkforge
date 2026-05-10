"""Configuration for zkforge."""
import os
import yaml

DEFAULT = {
    "zkforge": {"device_id": 0, "log_level": "info", "field": "bn254"},
    "prover": {"system": "groth16", "batch_size": 1024},
    "gpu": {"ntt_threads": 256, "msm_window_bits": 16},
}

class Config:
    def __init__(self, path=None):
        self.path = path or "configs/zkforge.yaml"
        self.data = DEFAULT.copy()
    def load(self):
        if os.path.exists(self.path):
            with open(self.path) as f: self._merge(self.data, yaml.safe_load(f) or {})
        return self.data
    def get(self, key, default=None):
        v = self.data
        for k in key.split("."):
            if isinstance(v, dict) and k in v: v = v[k]
            else: return default
        return v
    def _merge(self, b, o):
        for k, v in o.items():
            if k in b and isinstance(b[k], dict) and isinstance(v, dict): self._merge(b[k], v)
            else: b[k] = v
