#!/usr/bin/env python3
"""Benchmark an installed Candidate only after exhaustive semantic equality."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import platform
import statistics
import sys
import time


ROOT = Path(__file__).resolve().parents[1]


def load_oracle():
    path = ROOT / "upstream" / "oracle" / "roman" / "__init__.py"
    spec = importlib.util.spec_from_file_location("benchmark_roman_oracle", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load frozen Oracle")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def percentile_95(values):
    ordered = sorted(values)
    return ordered[max(0, math.ceil(len(ordered) * 0.95) - 1)]


def measure(function, inputs, samples, iterations, warmup):
    def one_sample():
        started = time.perf_counter_ns()
        for _ in range(iterations):
            for value in inputs:
                function(value)
        elapsed = time.perf_counter_ns() - started
        return elapsed / (iterations * len(inputs))

    for _ in range(warmup):
        one_sample()
    raw = [one_sample() for _ in range(samples)]
    return {
        "raw_ns_per_call": raw,
        "median_ns_per_call": statistics.median(raw),
        "p95_ns_per_call": percentile_95(raw),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--samples", type=int, default=15)
    parser.add_argument("--iterations", type=int, default=10)
    parser.add_argument("--warmup", type=int, default=3)
    args = parser.parse_args()

    import roman as candidate

    oracle = load_oracle()
    integers = list(range(5000))
    numerals = [oracle.toRoman(value) for value in integers]
    assert [candidate.toRoman(value) for value in integers] == numerals
    assert [oracle.fromRoman(value) for value in numerals] == integers
    assert [candidate.fromRoman(value) for value in numerals] == integers

    cases = {}
    for name, inputs in (("toRoman", integers), ("fromRoman", numerals)):
        oracle_result = measure(
            getattr(oracle, name), inputs, args.samples, args.iterations, args.warmup
        )
        candidate_result = measure(
            getattr(candidate, name), inputs, args.samples, args.iterations, args.warmup
        )
        candidate_result["oracle_over_candidate_median"] = (
            oracle_result["median_ns_per_call"]
            / candidate_result["median_ns_per_call"]
        )
        cases[name] = {"oracle": oracle_result, "candidate": candidate_result}

    artifact = args.artifact.resolve()
    report = {
        "schema": 1,
        "semantic_equality": "PASS exhaustive integers 0..4999",
        "oracle": "roman==5.2 frozen source",
        "candidate_distribution": "fast-roman-rs==0.1.0",
        "artifact": str(artifact),
        "artifact_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
        "python": sys.version,
        "implementation": platform.python_implementation(),
        "os": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu_count": os.cpu_count(),
        "inputs_per_iteration": len(integers),
        "iterations": args.iterations,
        "samples": args.samples,
        "warmup": args.warmup,
        "cases": cases,
    }
    args.output_json.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    rows = []
    for name, result in cases.items():
        rows.append(
            "| {name} | {oracle:.1f} | {candidate:.1f} | {p95:.1f} | {ratio:.2f}x |".format(
                name=name,
                oracle=result["oracle"]["median_ns_per_call"],
                candidate=result["candidate"]["median_ns_per_call"],
                p95=result["candidate"]["p95_ns_per_call"],
                ratio=result["candidate"]["oracle_over_candidate_median"],
            )
        )
    markdown = "\n".join(
        (
            "# Benchmark Evidence",
            "",
            "Semantic equality: **PASS**, exhaustive integers `0..4999` before timing.",
            "",
            "| Case | Oracle median ns/call | Candidate median ns/call | Candidate p95 ns/call | Oracle/Candidate median |",
            "|---|---:|---:|---:|---:|",
            *rows,
            "",
            "- Oracle: `roman==5.2` frozen source",
            "- Candidate: `fast-roman-rs==0.1.0` installed wheel",
            "- Artifact SHA256: `{}`".format(report["artifact_sha256"]),
            "- Python: `{}`".format(sys.version.splitlines()[0]),
            "- OS/machine: `{}` / `{}`".format(report["os"], report["machine"]),
            "- Inputs per iteration: `{}`; iterations: `{}`; samples: `{}`; warmup: `{}`".format(
                len(integers), args.iterations, args.samples, args.warmup
            ),
            "",
            "Raw samples are retained in the paired JSON artifact. Results describe only this artifact and host; no universal speed claim is made.",
            "",
        )
    )
    args.output_md.write_text(markdown, encoding="utf-8")
    print("benchmark: PASS semantic equality and timing")


if __name__ == "__main__":
    main()
