# Contributing a module

Every module published in the [integration store](https://aetheris.enterprise/store)
is an **accepted pull request** in this repository. This guide explains the
end-to-end flow.

## Flow

1. **Fork and branch.** Fork `aetheris-project/aetheris-addons`, create a
   branch named `addon/<module-id>`.
2. **Create the module.** Add a folder `addons/<module-id>/` with:
   - `manifest.json` (schema: `docs/manifest-schema.md`)
   - `src/index.ts` implementing the relevant contract from `types/index.ts`
   - `README.md` documenting setup and environment variables
   - tests under `tests/` when the logic is non-trivial
3. **Register it.** Add the module to the `addons` array in `store.json`
   (copy the `manifest.json` top-level fields plus a `state: "pending"`).
4. **Validate locally.**
   ```bash
   python tools/validate.py
   npm run typecheck
   python -m pytest -q
   ```
5. **Open the pull request.** CI runs the same checks. A maintainer reviews
   the implementation, security and documentation.
6. **Merge.** Once merged, the module's `state` becomes `accepted`, the store
   registry is updated and the module appears on the website store within the
   cache window.

## Rules

- Modules must not import platform internals; the contracts in `types/` are
  the only allowed dependency.
- No third-party runtime dependencies: use the platform `fetch` and standard
  library equivalents. If a dependency is unavoidable, discuss it in the PR.
- Secrets (API keys, webhook signatures) are always read from environment
  variables at runtime, never committed.
- `manifest.json` must be valid or CI fails.
- Keep the README honest: document rate limits, idempotency and failure modes.

## Review checklist

| Check | Done |
| --- | --- |
| Manifest schema valid and folder name matches `id` |  |
| Entry point implements the documented contract |  |
| Errors are typed and idempotent |  |
| No secrets in the diff |  |
| README covers setup, env vars and failure modes |  |
| `store.json` includes the module |  |

## See also

- [Manifest schema](docs/manifest-schema.md)
- [Module contracts](types/index.ts)
- [Template addon](templates/gateway-starter/)
