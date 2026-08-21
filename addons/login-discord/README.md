# Discord Sign-In Addon

Allow users to sign in to the Aetheris control panel with their Discord account.

## Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.
2. Under **OAuth2**, note the **Client ID** and generate a **Client Secret**.
3. Add a redirect URI: `https://your-domain.com/api/auth/callback/discord`.
4. Under **OAuth2 > Scopes**, ensure `identify` and `email` are selected.
5. Open **Admin Panel > Settings > Discord OAuth** and enter the Client ID and Client Secret.
6. Enable the addon and the "Continue with Discord" button will appear on the login page.

## Configuration keys

| Key | Description |
|---|---|
| `discord_oauth.clientId` | Discord application Client ID |
| `discord_oauth.clientSecret` | Discord application Client Secret |

## Scopes requested

- `identify` - User ID, username, avatar
- `email` - User email address (requires the email OAuth2 scope to be enabled in the Discord developer portal)

## Notes

- Discord only provides the email if the user has one verified and the `email` scope is requested.
- The user's display name is their Discord `global_name` (or `username` if no global name is set).
