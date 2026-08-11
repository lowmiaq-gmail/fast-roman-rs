# Frozen Upstream Contract

## Identity

- GitHub: `zopefoundation/roman`
- PyPI distribution: `roman`
- exact version: `5.2`
- tag: `5.2`
- annotated tag object: `92fc4842e7bb61cde06bea62d1860d6afbbee362`
- peeled commit: `a443357af7d7050ad6a0ec369fa73a1b9f14a558`
- Python: `>=3.10`
- runtime dependencies: none
- license: ZPL-2.1
- package: `roman`
- console script: `roman = roman:main`
- typing: inline annotations plus `roman/py.typed`

## Immutable PyPI artifacts

| Artifact | SHA256 |
|---|---|
| `roman-5.2-py3-none-any.whl` | `89d3b47400388806d06ff77ea77c79ab080bc127820dea6bf34e1f1c1b8e676e` |
| `roman-5.2.tar.gz` | `275fe9f46290f7d0ffaea1c33251b92b8e463ace23660508ceef522e7587cb6f` |

The sdist and wheel are the frozen Oracle artifacts. Candidate code must never be imported into the Oracle process.

## Source and tests

- Upstream implementation: tag `5.2`, `src/roman/__init__.py`.
- Complete official suite: tag `5.2`, `src/tests.py`.
- The official suite is run unfiltered against the Candidate. No test deletion, selection, or semantic edits are allowed.
- Candidate-only tests add contract boundaries not asserted by the official suite; they do not replace it.

## Packaging contract

Upstream installs one regular package named `roman`, a `py.typed` marker, and a `roman` console script. It does not provide `roman.__main__`; therefore `python -m roman` fails with Python's normal missing-`roman.__main__` error. There are no plugin entry points, optional dependencies, data files beyond typing/license metadata, environment behavior, file caches, warnings, or logging.

## Replacement distribution policy

- Replacement distribution: `fast-roman-rs==0.1.0`.
- Installed import namespace and console command remain `roman`.
- Native wheels: CPython abi3, minimum CPython 3.10, for supported Linux/macOS/Windows targets.
- Universal fallback: same name/version/metadata, `py3-none-any`, for PyPy and unsupported platforms.
- Both artifact families require Python `>=3.10` and contain no runtime dependency.
- PyPI and GitHub Release must use one immutable validated artifact set from one commit.
