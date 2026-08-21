/**
 * Aetheris Addon: Discord Sign-In
 *
 * Registers an OAuth 2.0 flow for Discord authentication.
 * Configuration is read from the Admin Panel settings store
 * (keys: discord_oauth.clientId, discord_oauth.clientSecret).
 */

export interface DiscordAddonConfig {
  clientId: string;
  clientSecret: string;
  redirectUri: string;
}

export interface DiscordTokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  refresh_token: string;
  scope: string;
}

export interface DiscordUser {
  id: string;
  username: string;
  discriminator: string;
  global_name: string | null;
  avatar: string | null;
  email: string | null;
  verified: boolean;
}

const DISCORD_AUTH_URL = "https://discord.com/api/oauth2/authorize";
const DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token";
const DISCORD_USER_URL = "https://discord.com/api/users/@me";
const SCOPES = ["identify", "email"];

export function buildDiscordAuthUrl(config: DiscordAddonConfig, state: string): string {
  const params = new URLSearchParams({
    client_id: config.clientId,
    redirect_uri: config.redirectUri,
    response_type: "code",
    scope: SCOPES.join(" "),
    state
  });
  return `${DISCORD_AUTH_URL}?${params.toString()}`;
}

export async function exchangeDiscordCode(
  config: DiscordAddonConfig,
  code: string
): Promise<DiscordTokenResponse> {
  const response = await fetch(DISCORD_TOKEN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: config.clientId,
      client_secret: config.clientSecret,
      grant_type: "authorization_code",
      code,
      redirect_uri: config.redirectUri
    })
  });

  if (!response.ok) {
    throw new Error(`Discord token exchange failed: ${response.status}`);
  }

  return response.json() as Promise<DiscordTokenResponse>;
}

export async function fetchDiscordUser(accessToken: string): Promise<DiscordUser> {
  const response = await fetch(DISCORD_USER_URL, {
    headers: { Authorization: `Bearer ${accessToken}` }
  });

  if (!response.ok) {
    throw new Error(`Discord user fetch failed: ${response.status}`);
  }

  return response.json() as Promise<DiscordUser>;
}
