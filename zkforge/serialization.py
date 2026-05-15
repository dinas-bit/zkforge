"""Proof serialization — save/load proofs in standard formats."""
import json
import base64
import logging
from pathlib import Path

logger = logging.getLogger("zkforge.serialization")

class ProofSerializer:
    """Serialize and deserialize ZK proofs."""

    @staticmethod
    def to_json(proof: dict) -> str:
        """Serialize proof to JSON."""
        def convert(obj):
            if hasattr(obj, "__dict__"): return obj.__dict__
            return str(obj)
        return json.dumps(proof, default=convert, indent=2)

    @staticmethod
    def from_json(json_str: str) -> dict:
        return json.loads(json_str)

    @staticmethod
    def save(proof: dict, path: str):
        with open(path, "w") as f:
            f.write(ProofSerializer.to_json(proof))
        logger.info(f"Proof saved: {path}")

    @staticmethod
    def load(path: str) -> dict:
        with open(path) as f:
            return ProofSerializer.from_json(f.read())

    @staticmethod
    def to_snarkjs(proof: dict, public_inputs: list) -> dict:
        """Export in snarkjs-compatible format."""
        return {"pi_a": str(proof.get("a", "")), "pi_b": str(proof.get("b", "")),
                "pi_c": str(proof.get("c", "")), "public_signals": [str(x) for x in public_inputs]}
