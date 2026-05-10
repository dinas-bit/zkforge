"""CLI for zkforge."""
import argparse
import logging
import sys
from .prover import Groth16Prover, PLONKProver
from .config import Config

def main():
    parser = argparse.ArgumentParser(prog="zkforge", description="GPU-accelerated ZK proofs")
    sub = parser.add_subparsers(dest="command")

    prove_parser = sub.add_parser("prove", help="Generate proof")
    prove_parser.add_argument("--system", choices=["groth16", "plonk", "stark"], default="groth16")
    prove_parser.add_argument("--circuit", required=True)
    prove_parser.add_argument("--witness", required=True)

    verify_parser = sub.add_parser("verify", help="Verify proof")
    verify_parser.add_argument("--proof", required=True)
    verify_parser.add_argument("--vk", required=True)

    bench_parser = sub.add_parser("benchmark", help="Run benchmarks")
    bench_parser.add_argument("--system", default="groth16")
    bench_parser.add_argument("--size", type=int, default=1048576)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    logging.basicConfig(level=logging.INFO)
    print(f"zkforge: {args.command}")

if __name__ == "__main__": main()
