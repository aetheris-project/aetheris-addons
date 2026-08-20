# Discord notifications

Post embeds with server events and billing alerts to Discord webhooks.

## Setup

| Environment variable | Required | Purpose |
| --- | --- | --- |
| `DISCORD_WEBHOOK_URL` | yes | Discord webhook URL for the target channel |


## Usage

The module is loaded by the Aetheris control panel from the manifest entry
point. See `types/index.ts` for the contract it implements.

## Failure modes

- Non-2xx responses throw a typed error with the HTTP status.
- Requests time out after 15 seconds (10 for notifications).
- Webhook verification requires the configured signing secret.
