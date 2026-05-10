"""GPU memory pool for ZK operations."""
import logging

logger = logging.getLogger("zkforge.gpu_memory")

class MemoryPool:
    def __init__(self, device_id=0, pool_mb=4096):
        self.device_id = device_id
        self.pool_mb = pool_mb
        self.allocated = {}
    def alloc(self, name, size_mb):
        self.allocated[name] = size_mb
        return True
    def free(self, name):
        self.allocated.pop(name, None)
    def usage(self):
        return sum(self.allocated.values())
