# Webhook logger

Fan out platform events to arbitrary HTTP endpoints with retries.

## Setup

| Environment variable | Required | Purpose |
| --- | --- | --- |
| `WEBHOOK_LOGGER_TARGETS` | yes | Comma-separated list of target URLs |


## Usage

The module is loaded by the Aetheris control plane from the manifest entry
point. See `types/index.ts` for the contract it implements.

## Failure modes

- Non-2xx responses throw a typed error with the HTTP status.
- Requests time out after 15 seconds (10 for notifications).
- Webhook verification requires the configured signing secret.
