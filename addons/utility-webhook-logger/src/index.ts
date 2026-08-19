/**
 * Webhook logger - Aetheris utility module.
 *
 * Fans out platform events to arbitrary HTTP endpoints with retries.
 */

export interface WebhookTarget {
  url: string;
  secret?: string;
}

export class WebhookLogger {
  readonly id = "utility-webhook-logger";

  constructor(private readonly targets: WebhookTarget[]) {
    if (targets.length === 0) throw new Error("utility-webhook-logger: at least one target is required");
  }

  async dispatch(event: Record<string, unknown>): Promise<void> {
    for (const target of this.targets) {
      await this.postWithRetry(target, event);
    }
  }

  private async postWithRetry(target: WebhookTarget, event: Record<string, unknown>): Promise<void> {
    let lastError: Error | undefined;
    for (let attempt = 1; attempt <= 3; attempt += 1) {
      try {
        const response = await fetch(target.url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-Aetheris-Event": String(event.type ?? "unknown")
          },
          body: JSON.stringify(event),
          signal: AbortSignal.timeout(10_000)
        });
        if (response.ok) return;
        lastError = new Error(`utility-webhook-logger: HTTP ${response.status}`);
      } catch (cause) {
        lastError = cause instanceof Error ? cause : new Error(String(cause));
      }
      await new Promise((resolve) => setTimeout(resolve, 500 * attempt));
    }
    throw lastError ?? new Error("utility-webhook-logger: delivery failed");
  }
}
