/**
 * Braintree - Aetheris payment gateway module.
 *
 * Implements the PaymentGateway contract from types/index.ts using only
 * the platform fetch and environment variables. Dependency-free by design.
 */

import type { CheckoutSession, PaymentGateway, PaymentResult, RefundResult, WebhookEvent } from "../../../types/index.js";

interface GatewayConfig {
  baseUrl: string;
  apiKey: string;
  webhookSecret?: string;
}

export class BraintreeGateway implements PaymentGateway {
  readonly id = "gateway-braintree";
  private readonly config: GatewayConfig;

  constructor(config: GatewayConfig) {
    if (!config.apiKey) throw new Error("gateway-braintree: apiKey is required");
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
      throw new Error(`gateway-braintree: HTTP ${response.status} on ${path}`);
    }
    return response.json() as Promise<T>;
  }

  async createCheckout(amountCents: number, currency: string, metadata: Record<string, string>): Promise<CheckoutSession> {
    const session = await this.request<CheckoutSession>("/checkouts", {
      method: "POST",
      body: JSON.stringify({ amount_cents: amountCents, currency, metadata, payment_methods: ["card,paypal,venmo"] })
    });
    return session;
  }

  async capturePayment(sessionId: string): Promise<PaymentResult> {
    return this.request<PaymentResult>(`/checkouts/${sessionId}/capture`, { method: "POST" });
  }

  async refund(paymentId: string, amountCents?: number): Promise<RefundResult> {
    return this.request<RefundResult>("/refunds", {
      method: "POST",
      body: JSON.stringify({ payment_id: paymentId, amount_cents: amountCents })
    });
  }

  async verifyWebhook(payload: string, signature: string): Promise<WebhookEvent> {
    if (!this.config.webhookSecret) throw new Error("gateway-braintree: webhookSecret is not configured");
    // Provider-specific signature check goes here; never trust unsigned events.
    const expected = `sha256=${await crypto.subtle.digest("SHA-256", new TextEncoder().encode(this.config.webhookSecret + payload))}`;
    if (signature !== expected) throw new Error("gateway-braintree: invalid webhook signature");
    return JSON.parse(payload) as WebhookEvent;
  }
}
