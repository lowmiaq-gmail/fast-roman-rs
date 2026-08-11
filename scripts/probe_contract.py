#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys


def decode(case):
    kind = case["kind"]
    value = case.get("value")
    if kind in {"str", "int", "float", "bool", "none"}:
        return None if kind == "none" else value
    if kind == "bytes":
        return value.encode("ascii")
    if kind == "list":
        return value
    raise ValueError("unknown case kind: %s" % kind)


def observe(function, *args):
    try:
        result = function(*args)
    except Exception as error:
        return {
            "outcome": "error",
            "type": type(error).__name__,
            "module": type(error).__module__,
            "message": str(error),
            "args": list(error.args),
        }
    return {"outcome": "return", "type": type(result).__name__, "value": result}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--module-root", type=Path)
    args = parser.parse_args()
    if args.module_root:
        sys.path.insert(0, str(args.module_root.resolve()))
    import roman

    records = []
    with args.corpus.open(encoding="utf-8") as handle:
        for line in handle:
            case = json.loads(line)
            value = decode(case)
            if case["function"] == "toRoman":
                records.append(observe(roman.toRoman, value))
            else:
                special = decode(case["special"])
                records.append(observe(roman.fromRoman, value, special))
    args.output.write_text(
        "\n".join(json.dumps(item, sort_keys=True) for item in records) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
