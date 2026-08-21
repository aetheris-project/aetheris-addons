/**
 * Aetheris Addon: Apple Sign-In
 *
 * Registers an OAuth 2.0 / OIDC flow for Apple authentication.
 * Configuration is read from the Admin Panel settings store
 * (keys: apple_oauth.teamId, apple_oauth.clientId, apple_oauth.keyId, apple_oauth.privateKey).
 */

export interface AppleAddonConfig {
  teamId: string;
  clientId: string;
  keyId: string;
  privateKey: string;
  redirectUri: string;
}

export interface AppleTokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  refresh_token?: string;
  id_token: string;
}

export interface AppleUserInfo {
  sub: string;
  email?: string;
  name?: {
    firstName?: string;
    lastName?: string;
  };
}

const APPLE_AUTH_URL = "https://appleid.apple.com/auth/authorize";
const APPLE_TOKEN_URL = "https://appleid.apple.com/auth/token";

/**
 * Generate the client_secret JWT required by Apple's token endpoint.
 * Apple uses ES256 (ECDSA with P-256 and SHA-256).
 */
export function generateAppleClientSecret(config: AppleAddonConfig): string {
  // In production, this uses jose library to sign with the .p8 private key.
  // The JWT has the following claims:
  const header = { alg: "ES256", kid: config.keyId };
  const payload = {
    iss: config.teamId,
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + 15777000, // 6 months
    aud: "https://appleid.apple.com",
    sub: config.clientId
  };

  // Placeholder: in production, sign with ES256 using the .p8 private key.
  return btoa(JSON.stringify(header)) + "." + btoa(JSON.stringify(payload)) + ".signature";
}

export function buildAppleAuthUrl(config: AppleAddonConfig, state: string): string {
  const params = new URLSearchParams({
    client_id: config.clientId,
    redirect_uri: config.redirectUri,
    response_type: "code id_token",
    scope: "name email",
    response_mode: "form_post",
    state
  });
  return `${APPLE_AUTH_URL}?${params.toString()}`;
}

export async function exchangeAppleCode(
  config: AppleAddonConfig,
  code: string
): Promise<AppleTokenResponse> {
  const clientSecret = generateAppleClientSecret(config);

  const response = await fetch(APPLE_TOKEN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      code,
      client_id: config.clientId,
      client_secret: clientSecret,
      redirect_uri: config.redirectUri,
      grant_type: "authorization_code"
    })
  });

  if (!response.ok) {
    throw new Error(`Apple token exchange failed: ${response.status}`);
  }

  return response.json() as Promise<AppleTokenResponse>;
}
