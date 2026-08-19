# Module manifest schema

Every module ships a `manifest.json`. The schema is enforced by
`tools/validate.py` in CI, so a pull request with an invalid manifest cannot
be merged.

```json
{
  "id": "gateway-coinbase",
  "name": "Coinbase Commerce",
  "category": "payment-gateway",
  "version": "1.0.0",
  "author": {
    "name": "Leonardo Galli",
    "github": "Leo-Galli"
  },
  "license": "MIT",
  "entry": "src/index.ts",
  "requires": ["billing"],
  "description": "Accept crypto payments through Coinbase Commerce.",
  "documentation": "README.md"
}
```

## Fields

| Field | Type | Required | Rules |
| --- | --- | --- | --- |
| `id` | string | yes | kebab-case, must equal the folder name |
| `name` | string | yes | non-empty human-readable name |
| `category` | string | yes | one of `payment-gateway`, `notification`, `storage`, `utility`, `panel` |
| `version` | string | yes | semantic version `MAJOR.MINOR.PATCH` |
| `author` | object | yes | `{ "name": string, "github": string }` |
| `license` | string | yes | SPDX identifier (e.g. `MIT`) |
| `entry` | string | yes | main entry relative to the module folder, must exist |
| `requires` | array | no | platform features: `billing`, `vncConsole`, `pterodactyl`, `proxmox`, `virtfusion`, `registrars` |
| `description` | string | yes | one-line description shown in the store |
| `documentation` | string | no | relative path to the module README, must exist |

## Categories

| Category | Implements | Purpose |
| --- | --- | --- |
| `payment-gateway` | `PaymentGateway` | Charge, capture, refund and verify webhooks |
| `notification` | `NotificationChannel` | Deliver alerts to external services |
| `storage` | `StorageDriver` | Object storage for backups and artifacts |
| `utility` | - | Reusable helpers (logging, monitoring, webhooks) |
| `panel` | - | Admin panel UI extensions |

## Validation

```bash
python tools/validate.py addons/<id>
```

Validates the manifest schema, entry/documentation existence, folder-name
match and `store.json` consistency.
