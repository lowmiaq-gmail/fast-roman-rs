# fast-roman-rs 0.1.0

Initial production release replacing frozen upstream `roman==5.2`.

- Rust-backed `toRoman` and `fromRoman` on compatible CPython via abi3 wheels.
- Same-version `py3-none-any` fallback for PyPy and unsupported platforms.
- Preserved `roman` namespace, signatures, exception hierarchy, regex/mapping globals, `py.typed`, and `roman` CLI.
- Complete upstream suite, Candidate contract suite, deterministic 10,000-case differential, fresh-wheel, sdist rebuild, and artifact inspection gates.

Install with `python -m pip install fast-roman-rs`. Do not co-install upstream `roman`, because both distributions own the same namespace and console command.
