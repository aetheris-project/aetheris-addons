# Coinbase Commerce

Accept crypto payments (BTC, ETH, USDC) through Coinbase Commerce.

## Setup

| Environment variable | Required | Purpose |
| --- | --- | --- |
| `COINBASE_API_KEY` | yes | Coinbase Commerce API key |
| `COINBASE_BASE_URL` | no | API base URL (defaults to https://api.commerce.coinbase.com) |
| `COINBASE_WEBHOOK_SECRET` | no | Shared webhook secret for signature verification |


## Usage

The module is loaded by the Aetheris control plane from the manifest entry
point. See `types/index.ts` for the contract it implements.

## Failure modes

- Non-2xx responses throw a typed error with the HTTP status.
- Requests time out after 15 seconds (10 for notifications).
- Webhook verification requires the configured signing secret.
