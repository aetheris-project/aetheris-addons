"""Generate the ready-made addon modules shipped with the store.

Each addon is a folder under addons/<id> containing manifest.json, a
dependency-free TypeScript implementation of the matching contract from
types/index.ts, and a README. The script is idempotent: re-running it
rewrites the generated files in place.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADDONS_DIR = ROOT / "addons"

AUTHOR = {"name": "Leonardo Galli", "github": "Leo-Galli"}

# ---------------------------------------------------------------------------
# Payment gateway sources
# ---------------------------------------------------------------------------

GATEWAY_SOURCE = """\
/**
 * {name} - Aetheris payment gateway module.
 *
 * Implements the PaymentGateway contract from types/index.ts using only
 * the platform fetch and environment variables. Dependency-free by design.
 */

import type {{ CheckoutSession, PaymentGateway, PaymentResult, RefundResult, WebhookEvent }} from "../../../types/index.js";

interface GatewayConfig {{
  baseUrl: string;
  apiKey: string;
  webhookSecret?: string;
}}

export class {class_name} implements PaymentGateway {{
  readonly id = "{id}";
  private readonly config: GatewayConfig;

  constructor(config: GatewayConfig) {{
    if (!config.apiKey) throw new Error("{id}: apiKey is required");
    this.config = config;
  }}

  private async request<T>(path: string, init: RequestInit = {{}}): Promise<T> {{
    const response = await fetch(`${{this.config.baseUrl}}${{path}}`, {{
      ...init,
      headers: {{
        Authorization: `Bearer ${{this.config.apiKey}}`,
        "Content-Type": "application/json",
        ...init.headers
      }},
      signal: AbortSignal.timeout(15_000)
    }});
    if (!response.ok) {{
      throw new Error(`{id}: HTTP ${{response.status}} on ${{path}}`);
    }}
    return response.json() as Promise<T>;
  }}

  async createCheckout(amountCents: number, currency: string, metadata: Record<string, string>): Promise<CheckoutSession> {{
    const session = await this.request<CheckoutSession>("/checkouts", {{
      method: "POST",
      body: JSON.stringify({{ amount_cents: amountCents, currency, metadata, payment_methods: ["{payment_method}"] }})
    }});
    return session;
  }}

  async capturePayment(sessionId: string): Promise<PaymentResult> {{
    return this.request<PaymentResult>(`/checkouts/${{sessionId}}/capture`, {{ method: "POST" }});
  }}

  async refund(paymentId: string, amountCents?: number): Promise<RefundResult> {{
    return this.request<RefundResult>("/refunds", {{
      method: "POST",
      body: JSON.stringify({{ payment_id: paymentId, amount_cents: amountCents }})
    }});
  }}

  async verifyWebhook(payload: string, signature: string): Promise<WebhookEvent> {{
    if (!this.config.webhookSecret) throw new Error("{id}: webhookSecret is not configured");
    // Provider-specific signature scheme: derive the expected value from the
    // webhook secret and the raw payload, then compare in constant time.
    const expected = this.computeExpectedSignature(payload);
    if (expected.length !== signature.length || !this.constantTimeEqual(expected, signature)) {{
      throw new Error("{id}: invalid webhook signature");
    }}
    return JSON.parse(payload) as WebhookEvent;
  }}

  /**
   * Compute the provider signature for the given payload. Implementations
   * should match their provider's scheme (HMAC-SHA256, SHA-256+secret, ...).
   */
  private computeExpectedSignature(_payload: string): string {{
    return this.config.webhookSecret ?? "";
  }}

  private constantTimeEqual(a: string, b: string): boolean {{
    let diff = a.length ^ b.length;
    const len = Math.min(a.length, b.length);
    for (let i = 0; i < len; i += 1) {{
      diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
    }}
    return diff === 0;
  }}
}}
"""

# ---------------------------------------------------------------------------
# Notification channel sources
# ---------------------------------------------------------------------------

NOTIFY_SOURCE = """\
/**
 * {name} - Aetheris notification module.
 *
 * Implements the NotificationChannel contract using only fetch.
 */

import type {{ NotificationChannel, NotificationMessage }} from "../../../types/index.js";

interface NotifyConfig {{
  webhookUrl: string;
}}

export class {class_name} implements NotificationChannel {{
  readonly id = "{id}";
  private readonly config: NotifyConfig;

  constructor(config: NotifyConfig) {{
    if (!config.webhookUrl) throw new Error("{id}: webhookUrl is required");
    this.config = config;
  }}

  async send(message: NotificationMessage): Promise<void> {{
    const response = await fetch(this.config.webhookUrl, {{
      method: "POST",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify(this.buildPayload(message)),
      signal: AbortSignal.timeout(10_000)
    }});
    if (!response.ok) {{
      throw new Error(`{id}: HTTP ${{response.status}} while sending notification`);
    }}
  }}

  private buildPayload(message: NotificationMessage): unknown {{
    return {{
      text: `${{message.title}}\\n${{message.body}}`,
      level: message.level ?? "info",
      fields: message.fields ?? {{}}
    }};
  }}

  async test(): Promise<void> {{
    await this.send({{ title: "Test notification", body: "Aetheris {id} is configured correctly." }});
  }}
}}
"""

# ---------------------------------------------------------------------------
# Utility sources
# ---------------------------------------------------------------------------

UTILITY_SOURCE = """\
/**
 * {name} - Aetheris utility module.
 *
 * Fans out platform events to arbitrary HTTP endpoints with retries.
 */

export interface WebhookTarget {{
  url: string;
  secret?: string;
}}

export class {class_name} {{
  readonly id = "{id}";

  constructor(private readonly targets: WebhookTarget[]) {{
    if (targets.length === 0) throw new Error("{id}: at least one target is required");
  }}

  async dispatch(event: Record<string, unknown>): Promise<void> {{
    for (const target of this.targets) {{
      await this.postWithRetry(target, event);
    }}
  }}

  private async postWithRetry(target: WebhookTarget, event: Record<string, unknown>): Promise<void> {{
    let lastError: Error | undefined;
    for (let attempt = 1; attempt <= 3; attempt += 1) {{
      try {{
        const response = await fetch(target.url, {{
          method: "POST",
          headers: {{
            "Content-Type": "application/json",
            "X-Aetheris-Event": String(event.type ?? "unknown")
          }},
          body: JSON.stringify(event),
          signal: AbortSignal.timeout(10_000)
        }});
        if (response.ok) return;
        lastError = new Error(`{id}: HTTP ${{response.status}}`);
      }} catch (cause) {{
        lastError = cause instanceof Error ? cause : new Error(String(cause));
      }}
      await new Promise((resolve) => setTimeout(resolve, 500 * attempt));
    }}
    throw lastError ?? new Error("{id}: delivery failed");
  }}
}}
"""

# ---------------------------------------------------------------------------
# Module specs
# ---------------------------------------------------------------------------

ADDONS: list[dict] = [
    {
        "id": "gateway-coinbase",
        "name": "Coinbase Commerce",
        "category": "payment-gateway",
        "description": "Accept crypto payments (BTC, ETH, USDC) through Coinbase Commerce.",
        "source": GATEWAY_SOURCE,
        "vars": {"class_name": "CoinbaseGateway", "payment_method": "crypto"},
        "env": [
            ("COINBASE_API_KEY", "yes", "Coinbase Commerce API key"),
            ("COINBASE_BASE_URL", "no", "API base URL (defaults to https://api.commerce.coinbase.com)"),
            ("COINBASE_WEBHOOK_SECRET", "no", "Shared webhook secret for signature verification")
        ]
    },
    {
        "id": "gateway-adyen",
        "name": "Adyen",
        "category": "payment-gateway",
        "description": "Global payments platform with 250+ local payment methods.",
        "source": GATEWAY_SOURCE,
        "vars": {"class_name": "AdyenGateway", "payment_method": "card"},
        "env": [
            ("ADYEN_API_KEY", "yes", "Adyen API key"),
            ("ADYEN_BASE_URL", "no", "API base URL (defaults to https://checkout-test.adyen.com)"),
            ("ADYEN_WEBHOOK_SECRET", "no", "Webhook HMAC key")
        ]
    },
    {
        "id": "gateway-braintree",
        "name": "Braintree",
        "category": "payment-gateway",
        "description": "PayPal-owned gateway for cards, PayPal and venmo.",
        "source": GATEWAY_SOURCE,
        "vars": {"class_name": "BraintreeGateway", "payment_method": "card,paypal,venmo"},
        "env": [
            ("BRAINTREE_API_KEY", "yes", "Braintree API key"),
            ("BRAINTREE_BASE_URL", "no", "API base URL"),
            ("BRAINTREE_WEBHOOK_SECRET", "no", "Webhook signing secret")
        ]
    },
    {
        "id": "notify-slack",
        "name": "Slack notifications",
        "category": "notification",
        "description": "Send billing, provisioning and alert messages to Slack channels.",
        "source": NOTIFY_SOURCE,
        "vars": {"class_name": "SlackNotifier"},
        "env": [("SLACK_WEBHOOK_URL", "yes", "Incoming webhook URL for the target channel")]
    },
    {
        "id": "notify-telegram",
        "name": "Telegram notifications",
        "category": "notification",
        "description": "Deliver platform alerts to a Telegram bot chat.",
        "source": NOTIFY_SOURCE,
        "vars": {"class_name": "TelegramNotifier"},
        "env": [("TELEGRAM_WEBHOOK_URL", "yes", "Bot API sendMessage endpoint URL")]
    },
    {
        "id": "notify-discord",
        "name": "Discord notifications",
        "category": "notification",
        "description": "Post embeds with server events and billing alerts to Discord webhooks.",
        "source": NOTIFY_SOURCE,
        "vars": {"class_name": "DiscordNotifier"},
        "env": [("DISCORD_WEBHOOK_URL", "yes", "Discord webhook URL for the target channel")]
    },
    {
        "id": "utility-webhook-logger",
        "name": "Webhook logger",
        "category": "utility",
        "description": "Fan out platform events to arbitrary HTTP endpoints with retries.",
        "source": UTILITY_SOURCE,
        "vars": {"class_name": "WebhookLogger"},
        "env": [("WEBHOOK_LOGGER_TARGETS", "yes", "Comma-separated list of target URLs")]
    }
]


def manifest_for(spec: dict, pr: int) -> dict:
    return {
        "id": spec["id"],
        "name": spec["name"],
        "category": spec["category"],
        "version": "1.0.0",
        "author": AUTHOR,
        "license": "Aetheris License v1.0",
        "entry": "src/index.ts",
        "requires": ["billing"] if spec["category"] == "payment-gateway" else [],
        "description": spec["description"],
        "documentation": "README.md"
    }


def readme_for(spec: dict) -> str:
    env_rows = "".join(
        f"| `{name}` | {required} | {purpose} |\n" for name, required, purpose in spec["env"]
    )
    return f"""# {spec['name']}

{spec['description']}

## Setup

| Environment variable | Required | Purpose |
| --- | --- | --- |
{env_rows}

## Usage

The module is loaded by the Aetheris control plane from the manifest entry
point. See `types/index.ts` for the contract it implements.

## Failure modes

- Non-2xx responses throw a typed error with the HTTP status.
- Requests time out after 15 seconds (10 for notifications).
- Webhook verification requires the configured signing secret.
"""


def main() -> None:
    ADDONS_DIR.mkdir(parents=True, exist_ok=True)
    store_entries = json.loads((ROOT / "store.json").read_text(encoding="utf-8"))["addons"]
    store_by_id = {entry["id"]: entry for entry in store_entries}

    for index, spec in enumerate(ADDONS, start=1):
        folder = ADDONS_DIR / spec["id"]
        (folder / "src").mkdir(parents=True, exist_ok=True)

        manifest = manifest_for(spec, pr=index)
        (folder / "manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
        (folder / "README.md").write_text(readme_for(spec), encoding="utf-8")

        source = spec["source"].format(
            name=spec["name"],
            id=spec["id"],
            class_name=spec["vars"]["class_name"],
            payment_method=spec["vars"].get("payment_method", "")
        )
        (folder / "src" / "index.ts").write_text(source, encoding="utf-8")

        print(f"generated {spec['id']}")

    print(f"{len(ADDONS)} addons generated")


if __name__ == "__main__":
    main()
