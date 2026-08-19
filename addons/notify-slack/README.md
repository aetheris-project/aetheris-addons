# Slack notifications

Send billing, provisioning and alert messages to Slack channels.

## Setup

| Environment variable | Required | Purpose |
| --- | --- | --- |
| `SLACK_WEBHOOK_URL` | yes | Incoming webhook URL for the target channel |


## Usage

The module is loaded by the Aetheris control plane from the manifest entry
point. See `types/index.ts` for the contract it implements.

## Failure modes

- Non-2xx responses throw a typed error with the HTTP status.
- Requests time out after 15 seconds (10 for notifications).
- Webhook verification requires the configured signing secret.
