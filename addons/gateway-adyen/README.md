# Adyen

Global payments platform with 250+ local payment methods.

## Setup

| Environment variable | Required | Purpose |
| --- | --- | --- |
| `ADYEN_API_KEY` | yes | Adyen API key |
| `ADYEN_BASE_URL` | no | API base URL (defaults to https://checkout-test.adyen.com) |
| `ADYEN_WEBHOOK_SECRET` | no | Webhook HMAC key |


## Usage

The module is loaded by the Aetheris control panel from the manifest entry
point. See `types/index.ts` for the contract it implements.

## Failure modes

- Non-2xx responses throw a typed error with the HTTP status.
- Requests time out after 15 seconds (10 for notifications).
- Webhook verification requires the configured signing secret.
