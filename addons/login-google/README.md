# Google Sign-In Addon

Allow users to sign in to the Aetheris control panel with their Google account via OAuth 2.0.

## Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
2. Create an **OAuth 2.0 Client ID** (type: Web application).
3. Add your redirect URI: `https://your-domain.com/api/auth/callback/google`.
4. Copy the **Client ID** and **Client Secret**.
5. Open **Admin Panel > Settings > Google OAuth** and paste the credentials.
6. Enable the addon and the "Continue with Google" button will appear on the login page.

## Configuration keys

| Key | Description |
|---|---|
| `google_oauth.clientId` | OAuth 2.0 Client ID from Google Cloud Console |
| `google_oauth.clientSecret` | OAuth 2.0 Client Secret from Google Cloud Console |

## Scopes requested

- `openid` - Required for OIDC
- `email` - User email address
- `profile` - User name and avatar
