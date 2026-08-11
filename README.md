# fast-roman-rs: fast Roman numerals for Python with Rust

Rust-backed drop-in replacement distribution for the frozen `roman==5.2` package.

It preserves the `roman` Python API and CLI while using a PyO3 Rust core on compatible CPython platforms. A same-version pure-Python wheel keeps the frozen contract available on supported PyPy and other platforms.

## Install fast-roman-rs

```bash
pip install fast-roman-rs
```

```python
import roman

assert roman.toRoman(972) == "CMLXXII"
assert roman.fromRoman("cMlxxii") == 972
```

The installed namespace, function signatures, exception hierarchy, regex globals, typing marker, and `roman` console command follow upstream 5.2. CPython selects a PyO3 abi3 wheel where available; PyPy and unsupported platforms use the same-version pure-Python fallback.

## Roman numeral CLI

```bash
roman 972
roman -r cMlxxii
```

## Migrate from roman 5.2

Remove the upstream distribution, install the replacement, and keep application imports unchanged:

```bash
python -m pip uninstall roman
python -m pip install fast-roman-rs
```

Do not install both distributions into the same environment because both own the `roman` namespace and console script.

## Roll back

```bash
python -m pip uninstall fast-roman-rs
python -m pip install roman==5.2
```

## Compatibility and verification

See [COMPATIBILITY.md](COMPATIBILITY.md) for the executable contract and [UPSTREAM-CONTRACT.md](UPSTREAM-CONTRACT.md) for immutable upstream evidence.

## Benchmark evidence

See [BENCHMARK.md](BENCHMARK.md). Measurements are published only after semantic equality and are scoped to the exact artifact and host.
