#!/usr/bin/env python3
import argparse
import json
import random
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEED = 20260812
CASE_COUNT = 10_000


def primitive(value):
    if value is None:
        return {"kind": "none"}
    if isinstance(value, bool):
        return {"kind": "bool", "value": value}
    if isinstance(value, int):
        return {"kind": "int", "value": value}
    if isinstance(value, float):
        return {"kind": "float", "value": value}
    if isinstance(value, bytes):
        return {"kind": "bytes", "value": value.decode("ascii")}
    if isinstance(value, list):
        return {"kind": "list", "value": value}
    return {"kind": "str", "value": value}


def generate_cases():
    rng = random.Random(SEED)
    cases = []
    for value in range(-100, 5_101):
        cases.append({"function": "toRoman", **primitive(value)})
    for value in (None, True, False, 1.0, "1"):
        cases.append({"function": "toRoman", **primitive(value)})

    special_values = [True, False, 0, 1, None, "yes"]
    fixed = ["", "N", "n", "I", "i", "IIII", "MMMM", "MMMMCMXCIX", "MMMMM", "I\n", "\n", "I\r\n", " N "]
    for value in fixed:
        for special in special_values:
            cases.append(
                {"function": "fromRoman", **primitive(value), "special": primitive(special)}
            )
    for value in (None, False, 0, [], b"I"):
        cases.append(
            {"function": "fromRoman", **primitive(value), "special": primitive(True)}
        )

    alphabet = "IVXLCDMNivxlcdmnQ0123 -_\n\r"
    while len(cases) < CASE_COUNT:
        value = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 22)))
        cases.append(
            {
                "function": "fromRoman",
                **primitive(value),
                "special": primitive(rng.choice(special_values)),
            }
        )
    return cases[:CASE_COUNT]


def run_probe(python, corpus, output, module_root=None):
    command = [
        str(python.absolute()),
        str(ROOT / "scripts" / "probe_contract.py"),
        "--corpus",
        str(corpus),
        "--output",
        str(output),
    ]
    if module_root:
        command.extend(["--module-root", str(module_root)])
    subprocess.run(command, check=True, cwd=tempfile.gettempdir())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--oracle-python", type=Path, required=True)
    parser.add_argument("--candidate-python", type=Path, required=True)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="fast-roman-diff-") as directory:
        temporary = Path(directory)
        corpus = temporary / "corpus.jsonl"
        oracle_output = temporary / "oracle.jsonl"
        candidate_output = temporary / "candidate.jsonl"
        cases = generate_cases()
        corpus.write_text(
            "\n".join(json.dumps(case, ensure_ascii=False) for case in cases) + "\n",
            encoding="utf-8",
        )
        run_probe(
            args.oracle_python,
            corpus,
            oracle_output,
            ROOT / "upstream" / "oracle",
        )
        run_probe(args.candidate_python, corpus, candidate_output)
        oracle_lines = oracle_output.read_text(encoding="utf-8").splitlines()
        candidate_lines = candidate_output.read_text(encoding="utf-8").splitlines()
        if oracle_lines != candidate_lines:
            for index, (oracle, candidate) in enumerate(zip(oracle_lines, candidate_lines)):
                if oracle != candidate:
                    raise AssertionError(
                        "differential mismatch at case %d: oracle=%s candidate=%s"
                        % (index, oracle, candidate)
                    )
            raise AssertionError("differential output cardinality mismatch")
        print("differential: PASS seed=%d cases=%d" % (SEED, len(cases)))


if __name__ == "__main__":
    main()
