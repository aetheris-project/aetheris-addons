/**
 * Discord notifications - Aetheris notification module.
 *
 * Implements the NotificationChannel contract using only fetch.
 */

import type { NotificationChannel, NotificationMessage } from "../../../types/index.js";

interface NotifyConfig {
  webhookUrl: string;
}

export class DiscordNotifier implements NotificationChannel {
  readonly id = "notify-discord";
  private readonly config: NotifyConfig;

  constructor(config: NotifyConfig) {
    if (!config.webhookUrl) throw new Error("notify-discord: webhookUrl is required");
    this.config = config;
  }

  async send(message: NotificationMessage): Promise<void> {
    const response = await fetch(this.config.webhookUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(this.buildPayload(message)),
      signal: AbortSignal.timeout(10_000)
    });
    if (!response.ok) {
      throw new Error(`notify-discord: HTTP ${response.status} while sending notification`);
    }
  }

  private buildPayload(message: NotificationMessage): unknown {
    return {
      text: `${message.title}\n${message.body}`,
      level: message.level ?? "info",
      fields: message.fields ?? {}
    };
  }

  async test(): Promise<void> {
    await this.send({ title: "Test notification", body: "Aetheris notify-discord is configured correctly." });
  }
}
