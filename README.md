# fast-roman-rs

Rust-backed drop-in replacement distribution for the frozen `roman==5.2` package.

```bash
pip install fast-roman-rs
```

```python
import roman

assert roman.toRoman(972) == "CMLXXII"
assert roman.fromRoman("cMlxxii") == 972
```

The installed namespace, function signatures, exception hierarchy, regex globals, typing marker, and `roman` console command follow upstream 5.2. CPython selects a PyO3 abi3 wheel where available; PyPy and unsupported platforms use the same-version pure-Python fallback.

See [COMPATIBILITY.md](COMPATIBILITY.md) for the executable contract and [UPSTREAM-CONTRACT.md](UPSTREAM-CONTRACT.md) for immutable upstream evidence.
