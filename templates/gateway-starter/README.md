# Gateway starter

Template for building a new payment gateway for the Aetheris platform.

## Setup

| Environment variable | Required | Purpose |
| --- | --- | --- |
| `STARTER_API_KEY` | yes | Gateway API key |
| `STARTER_BASE_URL` | no | API base URL (defaults to the gateway's production endpoint) |

## Usage

The platform instantiates the gateway through the manifest `entry` and calls
the `PaymentGateway` contract: `createCheckout`, `capturePayment`, `refund`
and `verifyWebhook`.

## Failure modes

- Non-2xx responses throw a typed error with the HTTP status.
- Requests time out after 15 seconds.
- Webhook verification must be implemented with your provider's signature
  scheme (see the platform wiki for the supported schemes).
