/**
 * Aetheris addon contracts.
 *
 * These are the canonical shapes every module implements. Modules must not
 * import platform internals; the contracts below are the only dependency.
 * They compile with `npm run typecheck` from the repository root.
 */

/** Manifest categories exposed in the store. */
export type AddonCategory =
  | "payment-gateway"
  | "notification"
  | "storage"
  | "utility"
  | "panel";

export interface AddonAuthor {
  name: string;
  github: string;
}

/**
 * The manifest.json shipped with every module. Validated by
 * tools/validate.py before a pull request is accepted.
 */
export interface AddonManifest {
  id: string;
  name: string;
  category: AddonCategory;
  version: string;
  author: AddonAuthor;
  license: string;
  entry: string;
  /** Platform features the module depends on (billing, vncConsole, ...). */
  requires?: string[];
  description: string;
  documentation?: string;
}

/* ------------------------------------------------------------------ */
/* Payment gateway contract                                            */
/* ------------------------------------------------------------------ */

export interface CheckoutSession {
  id: string;
  status: "pending" | "paid" | "expired";
  hostedUrl?: string;
  raw?: unknown;
}

export interface PaymentResult {
  id: string;
  status: "succeeded" | "failed" | "pending";
  amountCents: number;
  currency: string;
  raw?: unknown;
}

export interface RefundResult {
  id: string;
  status: "succeeded" | "failed";
  amountCents: number;
}

export interface WebhookEvent {
  type: string;
  payload: Record<string, unknown>;
}

export interface PaymentGateway {
  readonly id: string;
  createCheckout(
    amountCents: number,
    currency: string,
    metadata: Record<string, string>
  ): Promise<CheckoutSession>;
  capturePayment(sessionId: string): Promise<PaymentResult>;
  refund(paymentId: string, amountCents?: number): Promise<RefundResult>;
  verifyWebhook(payload: string, signature: string): Promise<WebhookEvent>;
}

/* ------------------------------------------------------------------ */
/* Notification channel contract                                       */
/* ------------------------------------------------------------------ */

export interface NotificationMessage {
  title: string;
  body: string;
  /** Optional key/value pairs rendered as an attachment. */
  fields?: Record<string, string>;
  level?: "info" | "success" | "warning" | "critical";
  channel?: string;
}

export interface NotificationChannel {
  readonly id: string;
  send(message: NotificationMessage): Promise<void>;
  test(): Promise<void>;
}

/* ------------------------------------------------------------------ */
/* Storage driver contract                                             */
/* ------------------------------------------------------------------ */

export interface StorageUpload {
  key: string;
  contentType: string;
  body: Uint8Array;
}

export interface StorageDriver {
  readonly id: string;
  put(upload: StorageUpload): Promise<void>;
  get(key: string): Promise<Uint8Array>;
  delete(key: string): Promise<void>;
  exists(key: string): Promise<boolean>;
}
