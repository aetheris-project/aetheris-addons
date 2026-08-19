/**
 * Gateway starter template.
 *
 * Copy this folder to addons/<your-id> and implement the PaymentGateway
 * contract. The platform provides no SDK: use fetch, read secrets from
 * environment variables and keep the module dependency-free.
 */

import type { CheckoutSession, PaymentGateway, PaymentResult, RefundResult, WebhookEvent } from "../../../types/index.js";

interface GatewayConfig {
  baseUrl: string;
  apiKey: string;
}

export class StarterGateway implements PaymentGateway {
  readonly id = "gateway-starter";
  private readonly config: GatewayConfig;

  constructor(config: GatewayConfig) {
    if (!config.apiKey) throw new Error("StarterGateway: apiKey is required");
    this.config = config;
  }

  private async request<T>(path: string, init: RequestInit = {}): Promise<T> {
    const response = await fetch(`${this.config.baseUrl}${path}`, {
      ...init,
      headers: {
        Authorization: `Bearer ${this.config.apiKey}`,
        "Content-Type": "application/json",
        ...init.headers
      },
      signal: AbortSignal.timeout(15_000)
    });
    if (!response.ok) {
      throw new Error(`StarterGateway: HTTP ${response.status} on ${path}`);
    }
    return response.json() as Promise<T>;
  }

  async createCheckout(amountCents: number, currency: string, metadata: Record<string, string>): Promise<CheckoutSession> {
    const session = await this.request<CheckoutSession>("/v1/checkouts", {
      method: "POST",
      body: JSON.stringify({ amount_cents: amountCents, currency, metadata })
    });
    return session;
  }

  async capturePayment(sessionId: string): Promise<PaymentResult> {
    return this.request<PaymentResult>(`/v1/checkouts/${sessionId}/capture`, { method: "POST" });
  }

  async refund(paymentId: string, amountCents?: number): Promise<RefundResult> {
    return this.request<RefundResult>("/v1/refunds", {
      method: "POST",
      body: JSON.stringify({ payment_id: paymentId, amount_cents: amountCents })
    });
  }

  async verifyWebhook(payload: string, signature: string): Promise<WebhookEvent> {
    // Validate the signature against your webhook secret, then parse.
    return JSON.parse(payload) as WebhookEvent;
  }
}
