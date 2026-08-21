# Apple Sign-In Addon

Allow users to sign in to the Aetheris control panel with their Apple ID.

## Setup

1. Go to [Apple Developer Console](https://developer.apple.com/account/resources/identifiers/list) and create an **App ID** with "Sign in with Apple" enabled.
2. Create a **Service ID** and associate it with the App ID.
3. Create a **Sign in with Apple key** and download the `.p8` private key file.
4. Note your **Team ID** from the membership page.
5. Configure the redirect URI: `https://your-domain.com/api/auth/callback/apple`.
6. Open **Admin Panel > Settings > Apple Sign-In** and enter all credentials.
7. Enable the addon and the "Continue with Apple" button will appear on the login page.

## Configuration keys

| Key | Description |
|---|---|
| `apple_oauth.teamId` | Apple Developer Team ID (10 characters) |
| `apple_oauth.clientId` | Service ID (e.g. `com.example.app`) |
| `apple_oauth.keyId` | Sign in with Apple key ID |
| `apple_oauth.privateKey` | Contents of the `.p8` private key file |

## Notes

- Apple only sends the user's email on first sign-in. Store it immediately.
- Apple may relay email addresses through `@privaterelay.appleid.com`.
- The client secret is a JWT signed with ES256 using the `.p8` private key.
