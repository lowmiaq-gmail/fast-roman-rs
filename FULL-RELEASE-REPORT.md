# Full Release Report

This is the immutable release dossier for `fast-roman-rs==0.1.0`. The release is
complete only when the guarded release workflow is green, the public PyPI URL
resolves, and the formal GitHub Release URL resolves. The workflow creates the
GitHub Release last, after public-index reinstall succeeds.

## Frozen target

- Upstream: `zopefoundation/roman==5.2`
- Commit: `a443357af7d7050ad6a0ec369fa73a1b9f14a558`
- Replacement: `fast-roman-rs==0.1.0`, import namespace `roman`

## Validated release candidate

- Implementation commit: `c51556dcf8326e7e9c50436e67f1c71d32063518`
- Cross-platform CI: https://github.com/lowmiaq-gmail/fast-roman-rs/actions/runs/31540572336
- Linux x86-64, macOS arm64, Windows x86-64, and PyPy fallback jobs passed.
- Each packaged-wheel lane ran the complete Candidate contract, all 8 unmodified
  upstream tests, and an isolated deterministic 10,000-case differential.
- Independent exact-archive verification repeated Rust fmt, Clippy with warnings
  denied, all-target tests, native/fallback/sdist inspection, `twine check`, fresh
  installs, the same Candidate/upstream/differential gates, and wheel-from-sdist.
- Semantic-equality-first benchmark evidence and raw samples are committed in
  `BENCHMARK.md` and `benchmarks/` without a universal speed claim.

## Public release evidence

- Release workflow: https://github.com/lowmiaq-gmail/fast-roman-rs/actions/workflows/release.yml
- PyPI: https://pypi.org/project/fast-roman-rs/0.1.0/
- GitHub Release: https://github.com/lowmiaq-gmail/fast-roman-rs/releases/tag/v0.1.0

The release workflow validates one artifact set, publishes it through PyPI OIDC,
reinstalls from the public index on supported CPython platforms and PyPy, and
then creates `v0.1.0` with those same distributions, benchmark evidence, and
`SHA256SUMS`. A missing URL or non-green workflow means this report is not a
completion claim.
