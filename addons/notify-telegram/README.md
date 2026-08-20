# Telegram notifications

Deliver platform alerts to a Telegram bot chat.

## Setup

| Environment variable | Required | Purpose |
| --- | --- | --- |
| `TELEGRAM_WEBHOOK_URL` | yes | Bot API sendMessage endpoint URL |


## Usage

The module is loaded by the Aetheris control panel from the manifest entry
point. See `types/index.ts` for the contract it implements.

## Failure modes

- Non-2xx responses throw a typed error with the HTTP status.
- Requests time out after 15 seconds (10 for notifications).
- Webhook verification requires the configured signing secret.
