# Full Release Report

Release status: **not released yet**. This report becomes final only after CI, independent verification, public PyPI reinstall, and formal GitHub Release all pass.

## Frozen target

- Upstream: `zopefoundation/roman==5.2`
- Commit: `a443357af7d7050ad6a0ec369fa73a1b9f14a558`
- Replacement: `fast-roman-rs==0.1.0`, import namespace `roman`

## Required evidence

- Rust fmt, Clippy with warnings denied, and all-target tests.
- Candidate contract and complete unmodified upstream tests.
- Isolated deterministic 10,000-case differential.
- Native/fallback/sdist artifact audit, fresh installs, and wheel-from-sdist.
- Linux/macOS/Windows packaged wheels and PyPy fallback.
- Semantic-equality-first benchmark with raw samples.
- Independent verifier result.
- PyPI OIDC publication and public-index reinstall.
- GitHub Release last with immutable distributions, benchmark evidence, and SHA256SUMS.

## Current local checkpoint

Rust gates, 31 Candidate tests, all 8 upstream tests, native/fallback 10,000-case differentials, canonical artifact inspection, twine checks, and sdist rebuild/install have passed locally. Cross-platform CI and all public release evidence remain pending and are not represented as complete.
