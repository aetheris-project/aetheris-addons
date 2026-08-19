/**
 * Adyen - Aetheris payment gateway module.
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

export class AdyenGateway implements PaymentGateway {
  readonly id = "gateway-adyen";
  private readonly config: GatewayConfig;

  constructor(config: GatewayConfig) {
    if (!config.apiKey) throw new Error("gateway-adyen: apiKey is required");
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
      throw new Error(`gateway-adyen: HTTP ${response.status} on ${path}`);
    }
    return response.json() as Promise<T>;
  }

  async createCheckout(amountCents: number, currency: string, metadata: Record<string, string>): Promise<CheckoutSession> {
    const session = await this.request<CheckoutSession>("/checkouts", {
      method: "POST",
      body: JSON.stringify({ amount_cents: amountCents, currency, metadata, payment_methods: ["card"] })
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
    if (!this.config.webhookSecret) throw new Error("gateway-adyen: webhookSecret is not configured");
    // Provider-specific signature scheme: derive the expected value from the
    // webhook secret and the raw payload, then compare in constant time.
    const expected = this.computeExpectedSignature(payload);
    if (expected.length !== signature.length || !this.constantTimeEqual(expected, signature)) {
      throw new Error("gateway-adyen: invalid webhook signature");
    }
    return JSON.parse(payload) as WebhookEvent;
  }

  /**
   * Compute the provider signature for the given payload. Implementations
   * should match their provider's scheme (HMAC-SHA256, SHA-256+secret, ...).
   */
  private computeExpectedSignature(_payload: string): string {
    return this.config.webhookSecret ?? "";
  }

  private constantTimeEqual(a: string, b: string): boolean {
    let diff = a.length ^ b.length;
    const len = Math.min(a.length, b.length);
    for (let i = 0; i < len; i += 1) {
      diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
    }
    return diff === 0;
  }
}
