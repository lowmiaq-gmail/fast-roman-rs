# Compatibility Matrix

Oracle: `roman==5.2`. Candidate distribution: `fast-roman-rs==0.1.0`. Installed namespace: `roman`.

## Public namespace

| Surface | Frozen behavior | Executable gate |
|---|---|---|
| `roman` | Regular package; module docstring `Convert to and from Roman numerals` | namespace/introspection test |
| `__author__` | exact Mark Pilgrim string | exact equality |
| `__copyright__` | exact multiline upstream value | exact equality |
| imported modules | public globals `argparse`, `re`, `sys` | identity/type checks |
| `romanNumeralMap` | exact 13-pair tuple, order preserved | exact equality/type |
| `romanNumeralPattern` | exact `re.Pattern`, pattern text, flags `re.UNICODE|re.VERBOSE` (`96`), 3 groups, empty groupindex | exact pattern/introspection plus corpus |
| typing | annotations are real builtins/`argparse.Namespace`; `py.typed` is packaged | annotations and artifact inspection |
| additive native internals | private `_native` only; no additive public non-underscore names | public-name equality |

## Classes

| Class | Bases and module | Behavior |
|---|---|---|
| `RomanError` | `Exception`, module `roman` | normal exception semantics |
| `OutOfRangeError` | `RomanError`, module `roman` | raised by out-of-range `toRoman` |
| `NotIntegerError` | `RomanError`, module `roman` | raised by non-`int` `toRoman` |
| `InvalidRomanNumeralError` | `RomanError`, module `roman` | raised by invalid/blank `fromRoman` |

## Functions and signatures

| Function | Exact signature | Frozen behavior |
|---|---|---|
| `toRoman` | `(n: int) -> str` | Requires `isinstance(n, int)`; therefore bool and int subclasses are accepted. Range is `0..4999`. Zero is `N`. Exact errors: `decimals cannot be converted` and `number out of range (must be 0..4999)`. |
| `fromRoman` | `(s: str, special_case: bool = True) -> int` | First applies Python truthiness, then `.upper()`. Falsy non-strings raise blank-input error; arbitrary truthy objects may work if `.upper()` returns a string. `N` maps to 0 only when `special_case` is truthy. Lowercase is accepted. One trailing LF is accepted because the public regex uses `$`; CRLF/double LF are rejected. Exact invalid message is `Invalid Roman numeral: {UPPERCASED_INPUT}`. |
| `parse_args` | `() -> argparse.Namespace` | Reads `sys.argv`; positional `number`; `-r/--reverse`; exact argparse help/error surface. |
| `main` | `() -> int` | Converts using `int()` or `fromRoman`, prints one line, and returns `0`; conversion exceptions are not swallowed. |

Function `__name__`, `__qualname__`, `__module__`, `__doc__`, `__annotations__`, `__defaults__`, and `__kwdefaults__` are part of the gate. The compatibility layer keeps these Python-visible properties exact while delegating validated conversion work to Rust.

## CLI and module entry

| Invocation | Contract |
|---|---|
| `roman 972` | stdout `CMLXXII\n`, exit 0 |
| `roman -r cMlxxii` | stdout `972\n`, exit 0 |
| `roman --help` | argparse usage, description, positional/options text, exit 0 |
| invalid forward input | native Python `int()` traceback/error boundary retained |
| invalid reverse input | upstream exception traceback/error boundary retained |
| `python -m roman` | fails because `roman.__main__` is intentionally absent |

## Verification matrix

- Rust: `cargo fmt --check`, Clippy all targets/features with warnings denied, all-target tests.
- Candidate: complete contract/CLI/artifact tests on native and fallback wheels.
- Upstream: unmodified complete `src/tests.py` against each Candidate artifact.
- Differential: isolated Oracle and Candidate processes, deterministic seed, at least 10,000 cases covering all integers near and beyond range, canonical numerals, lowercase, invalid permutations, newline boundaries, dynamic types, exception class/message, and `special_case` truthiness.
- Artifacts: native wheel, `py3-none-any` fallback wheel, and sdist; METADATA/WHEEL/RECORD/license/typing/entry-point inspection; wheel rebuilt from sdist.
- Platforms: packaged wheels on Linux x86-64/aarch64, macOS x86-64/arm64, Windows x86-64; fallback on PyPy where upstream supports it.
- Release: semantic equality before benchmark; independent verification; OIDC publish; fresh public-index reinstall; formal GitHub Release last with checksums.
