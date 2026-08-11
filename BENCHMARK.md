# Benchmark Evidence

Semantic equality: **PASS**, exhaustive integers `0..4999` before timing.

| Case | Oracle median ns/call | Candidate median ns/call | Candidate p95 ns/call | Oracle/Candidate median |
|---|---:|---:|---:|---:|
| toRoman | 365.3 | 114.8 | 171.5 | 3.18x |
| fromRoman | 1222.5 | 266.5 | 288.2 | 4.59x |

- Oracle: `roman==5.2` frozen source
- Candidate: `fast-roman-rs==0.1.0` installed wheel
- Artifact SHA256: `dc3852a77d611a118b5e80138b9aa08001a6079916c0222fda9a022d6a6a4208`
- Python: `3.14.6 (main, Jun 10 2026, 10:03:53) [Clang 21.0.0 (clang-2100.0.123.102)]`
- OS/machine: `macOS-26.5.2-arm64-arm-64bit-Mach-O` / `arm64`
- Inputs per iteration: `5000`; iterations: `10`; samples: `15`; warmup: `3`

Raw samples are retained in the paired JSON artifact. Results describe only this artifact and host; no universal speed claim is made.
