# Runtime Parameter Matrix

## Goal
Use this matrix to capture every local parameter that matters for parity with the original system and to avoid undocumented machine-specific drift.

## How to use it
- fill `configs/runtime-manifest.local.yaml` first;
- keep `memory/config.yaml` aligned with the memory section of the manifest;
- update this matrix when a new local dependency or operator command becomes required.

| Area | Parameter | Where to store it | Required | Safe in git | Notes |
|---|---|---|---|---|---|
| Workspace | Workspace root | `configs/runtime-manifest.local.yaml` | Yes | No | Keep local if it reveals absolute paths. |
| Workspace | OS and shell | `configs/runtime-manifest.local.yaml` | Yes | Yes | Example: `windows` and `powershell`. |
| Runtime | Python launcher | `configs/runtime-manifest.local.yaml` | Yes | Yes | Prefer the exact launcher the operator will use. |
| Runtime | Python version target | `configs/runtime-manifest.local.yaml` | Yes | Yes | Use a concrete version or supported range. |
| Runtime | Codex host mode | `configs/runtime-manifest.local.yaml` | Yes | Yes | Example: `desktop`. |
| Embeddings | Provider type | `configs/runtime-manifest.local.yaml` | Yes | Yes | Example: `ollama`. |
| Embeddings | Provider URL | `configs/runtime-manifest.local.yaml`, `memory/config.yaml` | Yes | Usually no | Public docs can show placeholders only. |
| Embeddings | Model name | `configs/runtime-manifest.local.yaml`, `memory/config.yaml` | Yes | Yes | Example: `nomic-embed-text-v2-moe`. |
| Memory | Vault path | `configs/runtime-manifest.local.yaml`, `memory/config.yaml` | Yes | No | This is the markdown source of truth. |
| Memory | Storage directory | `configs/runtime-manifest.local.yaml`, `memory/config.yaml` | Yes | No | Store indexes and caches here. |
| Memory | Chunk size | `memory/config.yaml` | Yes | Yes | Must match your retrieval expectations. |
| Memory | Chunk overlap | `memory/config.yaml` | Yes | Yes | Keep stable unless you rebaseline retrieval. |
| Memory | Top-k values | `memory/config.yaml` | Yes | Yes | Affects retrieval quality and latency. |
| Memory | Role include-paths | `memory/config.yaml` | Yes | Yes | Core part of parity. |
| Commands | Doctor command | `configs/runtime-manifest.local.yaml` | Yes | Yes | Must be the real operator command. |
| Commands | Health command | `configs/runtime-manifest.local.yaml` | Yes | Yes | Must be the real operator command. |
| Commands | Preflight command | `configs/runtime-manifest.local.yaml` | Yes | Yes | Use the working Python launcher. |
| Commands | Search command | `configs/runtime-manifest.local.yaml` | Yes | Yes | Prefer a single standard form. |
| Commands | Index command | `configs/runtime-manifest.local.yaml` | Yes | Yes | Document the rebuild entrypoint. |
| Commands | Finalize command | `configs/runtime-manifest.local.yaml` | Yes | Yes | Must point to the archival path. |
| Commands | Watch command | `configs/runtime-manifest.local.yaml` | No | Yes | Optional but recommended. |
| Access | Environment tiers | `configs/runtime-manifest.local.yaml`, `configs/data-access.template.yaml` | Yes | Yes | Keep production disabled by default. |
| Access | Approval rules | `configs/data-access.template.yaml` | Yes | Yes | Match the real operator approval posture. |
| Observability | Report location | `configs/runtime-manifest.local.yaml`, `configs/evals.template.yaml` | Yes | Yes | Keeps reports easy to find. |
| Recovery | Backup location | `configs/runtime-manifest.local.yaml`, `configs/recovery.template.yaml` | Yes | Usually no | Often local-only. |
| Recovery | Reindex-from-markdown policy | `configs/recovery.template.yaml` | Yes | Yes | Indexes are caches, not source of truth. |

## Minimum parity review
Before calling a new installation equivalent to the original system, verify:
- the same role and route model is published;
- the same memory topology is configured;
- the same command entrypoints exist and work;
- the same approval and production restrictions apply;
- the same recovery and observability expectations are documented.
