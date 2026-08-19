# Braintree

PayPal-owned gateway for cards, PayPal and venmo.

## Setup

| Environment variable | Required | Purpose |
| --- | --- | --- |
| `BRAINTREE_API_KEY` | yes | Braintree API key |
| `BRAINTREE_BASE_URL` | no | API base URL |
| `BRAINTREE_WEBHOOK_SECRET` | no | Webhook signing secret |


## Usage

The module is loaded by the Aetheris control plane from the manifest entry
point. See `types/index.ts` for the contract it implements.

## Failure modes

- Non-2xx responses throw a typed error with the HTTP status.
- Requests time out after 15 seconds (10 for notifications).
- Webhook verification requires the configured signing secret.
