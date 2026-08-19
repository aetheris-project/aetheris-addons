<p align="center">
  <img src="assets/icon.svg" alt="Aetheris" width="88">
</p>

<h1 align="center">Aetheris Addons</h1>

<p align="center">
  <strong>Modules and integrations for the Aetheris platform - store, contracts and accepted pull requests</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/TypeScript-5.6-blue?logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
  <img src="https://img.shields.io/badge/status-live-10B981" alt="Live">
</p>

---

Aetheris Addons is the extension layer of the Aetheris platform. Beyond the
theme system, anyone can ship **modules** (payment gateways, notification
channels, storage drivers, utilities) that plug into the control plane through
small, dependency-free TypeScript contracts.

**Every entry in the [integration store](https://aetheris.enterprise/store) is
an accepted pull request in this repository.** Nothing is published without
review.

## Repository layout

```text
aetheris-addons/
├── addons/                    # Published modules (one folder per module)
│   ├── gateway-coinbase/      #   example: Coinbase Commerce payment gateway
│   └── ...
├── docs/
│   └── manifest-schema.md     # Manifest reference
├── templates/
│   └── gateway-starter/       # Copy-paste starting point for a new gateway
├── types/
│   └── index.ts               # Module contracts (PaymentGateway, NotificationChannel, ...)
├── tools/
│   └── validate.py            # Manifest + store registry validator
├── tests/                     # Validator test suite (pytest)
└── store.json                 # Store registry consumed by the website
```

## Quickstart

```bash
# Validate every module and the store registry
python tools/validate.py

# Typecheck all module sources
npm install
npm run typecheck

# Run the validator test suite
python -m pytest -q
```

## Building a module

1. Copy `templates/gateway-starter/` to `addons/<module-id>/`.
2. Fill in `manifest.json` (see `docs/manifest-schema.md`).
3. Implement the contract from `types/index.ts`.
4. Add the module to `store.json`.
5. Validate, then open a pull request - see `CONTRIBUTING.md`.

## Published modules

| Module | Category | Author |
| --- | --- | --- |
| Coinbase Commerce | Payment gateway | Leonardo Galli |
| Adyen | Payment gateway | Leonardo Galli |
| Braintree | Payment gateway | Leonardo Galli |
| Slack notifications | Notification | Leonardo Galli |
| Telegram notifications | Notification | Leonardo Galli |
| Discord notifications | Notification | Leonardo Galli |
| Webhook logger | Utility | Leonardo Galli |

See `store.json` for the full registry and the website store for the live
catalog.

## Related repositories

- [aetheris-website](https://github.com/aetheris-project/aetheris-website) -
  marketing site, interactive demo and integration store
- [aetheris-app](https://github.com/aetheris-project/aetheris-app) - control
  plane core
- [aetheris-docs](https://github.com/aetheris-project/aetheris-docs) - wiki
  (Modules and integrations / Integration store pages)
- [aetheris-themes](https://github.com/aetheris-project/aetheris-themes) -
  theme guide and templates

## License

MIT for the addons; the platform core remains proprietary. See each module's
manifest for its license.
