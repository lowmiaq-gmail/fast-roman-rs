# Reuse Audit

## Decision

`BUILD` a complete replacement distribution named `fast-roman-rs`, version `0.1.0`, that installs the frozen upstream `roman` namespace and CLI for `roman==5.2`.

This is not an accelerator or API subset. The native artifact must preserve the complete frozen contract, while a same-version pure-Python wheel preserves supported PyPy and platforms without a compatible native wheel.

## Existing-project audit

- User-owned local and public repositories were checked first. Only the already-completed `fast-dotenv-rs` and `fast-rfc3339-validator-rs` replacements exist; there is no in-flight Roman implementation to adapt.
- PyPI project JSON for `fast-roman-rs` and `roman-rs` returned HTTP 404 before target creation.
- GitHub repository/code searches found no PyO3/Maturin distribution that installs the `roman` 5.2 namespace, signatures, exception hierarchy, regex globals, typing marker, and `roman` console script.
- Other Roman-numeral Python packages and Rust crates expose different names and APIs. They are algorithms or alternate products, not drop-in replacements.

## Production asset reuse

The requested `lowmiaq-gmail/fast-dotenv-rs/reusable/EXTRACTION-REPORT.md` is not present in the local checkout or the pipeline workspace, so it cannot be copied or cited as a file. The validated production patterns already reused by library 2 remain applicable:

- PyO3 abi3 with a Maturin mixed project.
- Native CPython wheel plus same-version universal fallback wheel.
- Oracle and Candidate isolation in separate virtual environments/processes.
- Deterministic 10,000-case differential testing.
- Fresh-wheel and wheel-from-sdist tests.
- Exact artifact inspector for METADATA, WHEEL, RECORD, licenses, names, versions, and duplicate paths.
- Linux/macOS/Windows native wheel matrix and public-index reinstall gates.
- GitHub Actions OIDC Trusted Publishing with immutable artifacts.
- SHA256 evidence and formal GitHub Release only after public PyPI reinstall.
- README, CHANGELOG, BENCHMARK, COMPATIBILITY, THIRD_PARTY_NOTICES, SEO-REPORT, and FULL-RELEASE-REPORT.

Library-2 domain code, RFC3339 fixtures, semantics, and benchmark numbers are explicitly excluded from reuse.

## Why `roman==5.2`

- Stable, small, pure-Python upstream with no runtime dependency.
- Python `>=3.10`, with explicit CPython and PyPy classifiers.
- One package, one complete upstream test module, two conversion functions, four exception classes, a regex/mapping contract, and one console script.
- Rust is valuable for the conversion/validation loop, while a thin Python layer can exactly preserve dynamic `isinstance`, truthiness, `.upper()`, annotations, exceptions, argparse, and compiled-regex behavior.
- The complete frozen contract is tractable; no partial acceleration is required.

## Rejected/deferred alternatives

- `rfc3986-validator==0.1.1`: deferred because its public function returns a real `re.Match | None`, and its large public compiled-regex/match-group contract makes it less suitable for the next easiest complete replacement.
- `tomli-w==1.2.0`: deferred because exact nested TOML formatting, ordering, escaping, float, date/time, and error behavior create a larger combination surface.

## License

Upstream is ZPL-2.1. The replacement will retain `LICENSE.txt`, `COPYRIGHT.txt`, attribution, source notices, and a `THIRD_PARTY_NOTICES.md`. New Rust/glue code will not remove or relabel upstream-covered material.
