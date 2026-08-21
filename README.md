<p align="center">
  <img src="assets/icon.svg" alt="Aetheris Addons" width="88" style="filter: drop-shadow(0 0 20px rgba(14,165,233,0.55))">
</p>

<h1 align="center">Aetheris Addons</h1>

<p align="center">
  <strong>Extension layer of the Aetheris platform — payment gateways, notification channels, SSO providers and utilities</strong>
</p>

<p align="center">
  <a href="https://aetheris-web.vercel.app/store"><img src="https://img.shields.io/badge/Live-Store-10B981?style=for-the-badge&logo=vercel&logoColor=white" alt="Store"></a>
  <a href="https://aetheris-docs.vercel.app/wiki/store"><img src="https://img.shields.io/badge/Docs-Store%20Guide-0EA5E9?style=for-the-badge&logo=readthedocs&logoColor=white" alt="Docs"></a>
  <a href="https://discord.gg/6GcfebuT2A"><img src="https://img.shields.io/badge/Discord-Help-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/TypeScript-5.6-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Node.js-20-339933?style=flat-square&logo=nodedotjs&logoColor=white" alt="Node">
  <img src="https://img.shields.io/badge/Contracts-Typed-EC4899?style=flat-square" alt="Typed">
  <img src="https://img.shields.io/badge/CI-Validated-10B981?style=flat-square&logo=githubactions&logoColor=white" alt="CI">
  <img src="https://img.shields.io/badge/Published-10%2B%20Modules-F59E0B?style=flat-square" alt="Modules">
  <img src="https://img.shields.io/badge/License-AGPLv3-10B981?style=flat-square" alt="License">
</p>

---

<br>

> **Every entry in the Aetheris Integration Store is an accepted pull request
> in this repository.** Nothing ships without review. Modules are tiny,
> dependency-free TypeScript files that plug into the Aetheris control panel
> via small typed contracts — payment gateways, SMS/discord/telegram/slack
> notifiers, SSO login providers (Google, Discord, Apple), utility webhooks
> and storage drivers — no monorepo fork required.
>
> Build → validate → open a PR → it lands in the store.

<br>

## ✨ Features

<table>
  <tr>
    <td width="33%" align="center" valign="top">
      <h3>🔌 4 module types</h3>
      <p>
        <strong>PaymentGateway</strong> — checkout providers<br>
        <strong>NotificationChannel</strong> — alerts & webhooks<br>
        <strong>LoginProvider</strong> — SSO / OAuth<br>
        <strong>Utility</strong> — one-off helpers
      </p>
    </td>
    <td width="33%" align="center" valign="top">
      <h3>📜 Typed contracts</h3>
      <p>Every module implements a pure interface from <code>types/index.ts</code>. Autocomplete + validation gate the store.</p>
    </td>
    <td width="33%" align="center" valign="top">
      <h3>✅ CI validation</h3>
      <p>Python stdlib validator checks manifest schema, registry integrity, TypeScript types and unique module IDs.</p>
    </td>
  </tr>
  <tr>
    <td align="center" valign="top">
      <h3>🚀 Starter template</h3>
      <p><code>templates/gateway-starter/</code> — copy → rename → fill the 3 files. Zero boilerplate, full working example.</p>
    </td>
    <td align="center" valign="top">
      <h3>🏪 Live store</h3>
      <p><code>store.json</code> registry is consumed directly by the website and the control-panel Addon browser.</p>
    </td>
    <td align="center" valign="top">
      <h3>🔐 Sandboxed</h3>
      <p>Modules run inside a typed shim. No raw globals, signed manifests, install-time human review.</p>
    </td>
  </tr>
</table>

<br>

## 🚀 Quick Start

```bash
# 1. Install tooling for TS typecheck
npm install

# 2. Validate EVERYTHING — manifests, registry, types
python tools/validate.py

# 3. Typecheck module sources
npm run typecheck

# 4. Run the validator pytest suite
python -m pytest -q
```

### Building a new module — six steps

1. Copy `templates/gateway-starter/` → `addons/<your-module-id>/`
2. Rename + fill in `manifest.json` (see [docs/manifest-schema.md](docs/manifest-schema.md))
3. Implement the typed contract exported by `types/index.ts` in `src/index.ts`
4. Register your module ID + metadata in `store.json`
5. Run `python tools/validate.py` + `npm run typecheck` → both green
6. Read `CONTRIBUTING.md` and open a pull request 🎉

<br>

## 📦 Published Modules

| Module | Category | Author | Tagline |
|---|---|---|---|
| **Coinbase Commerce** | 💳 Payment Gateway | Leonardo Galli | Crypto checkout with on-chain confirmations |
| **Adyen** | 💳 Payment Gateway | Leonardo Galli | Enterprise cards + Klarna + iDEAL + local methods |
| **Braintree** | 💳 Payment Gateway | Leonardo Galli | PayPal, Venmo, Apple Pay, Google Pay one-click |
| **Discord Login** | 🔐 SSO Provider | Leonardo Galli | OAuth2 "Continue with Discord" + guild-gated roles |
| **Google Login** | 🔐 SSO Provider | Leonardo Galli | Google Identity OAuth2 with hosted-domain gating |
| **Apple Login** | 🔐 SSO Provider | Leonardo Galli | Sign in with Apple + private-key JWS flow |
| **Discord Notify** | 🔔 Notification | Leonardo Galli | Webhook embeds into any channel on billing events |
| **Slack Notify** | 🔔 Notification | Leonardo Galli | Block-kit messages to Slack channels or users |
| **Telegram Notify** | 🔔 Notification | Leonardo Galli | Bot messages to users/groups via HTTP API |
| **Webhook Logger** | 🛠 Utility | Leonardo Galli | Request/response logger, replay and export (debug tool) |

Live catalog with install instructions and screenshots:
**[aetheris-web.vercel.app/store](https://aetheris-web.vercel.app/store)**

<br>

## 🧩 Repository Layout

```text
aetheris-addons/
├── addons/                        # Published modules — 1 folder per module
│   ├── gateway-adyen/             #   💳 Adyen payment gateway
│   ├── gateway-braintree/         #   💳 Braintree / PayPal
│   ├── gateway-coinbase/          #   💳 Coinbase Commerce
│   ├── login-apple/               #   🔐 Sign in with Apple
│   ├── login-discord/             #   🔐 Discord OAuth2
│   ├── login-google/              #   🔐 Google Identity
│   ├── notify-discord/            #   🔔 Discord webhook embeds
│   ├── notify-slack/              #   🔔 Slack block-kit
│   ├── notify-telegram/           #   🔔 Telegram bot
│   └── utility-webhook-logger/    #   🛠 Debug utility
├── docs/
│   └── manifest-schema.md         # Authoritative manifest JSON schema
├── templates/
│   └── gateway-starter/           # Copy-paste starting point (manifest + src + README)
├── types/
│   └── index.ts                   # Module contracts: PaymentGateway, NotificationChannel, LoginProvider, Utility
├── tools/
│   ├── validate.py                # Stdlib Python validator — manifest + registry + uniqueness
│   └── generate_addons.py         # Regenerate listing + store index
├── tests/                         # Validator pytest suite
├── store.json                     # 🏪 Registry consumed by website + control panel
├── tsconfig.json
├── package.json
└── CONTRIBUTING.md
```

<br>

## 🧪 Tests

```bash
# Python validator tests
python -m pip install pytest
python -m pytest -q

# TypeScript typecheck
npm install
npm run typecheck
```

---

<p align="center">
  <strong>Made with 💚 by <a href="https://github.com/Leo-Galli">Leonardo Galli</a></strong>
</p>

<p align="center">
  <a href="https://github.com/aetheris-project/aetheris-app">App</a>
  ·
  <a href="https://github.com/aetheris-project/aetheris-website">Website</a>
  ·
  <a href="https://github.com/aetheris-project/aetheris-themes">Themes</a>
  ·
  <a href="https://discord.gg/6GcfebuT2A">Discord</a>
  ·
  <a href="https://paypal.me/LeonardoGalliITA">Donate</a>
</p>

## 📄 License

Licensed under **GNU Affero General Public License v3.0 (AGPL-3.0)**.
See [LICENSE.md](LICENSE.md). You may use, study, modify and redistribute
for any purpose provided distributed or network-served modified versions
keep this license, preserve Leonardo Galli's copyright notice and release
source under AGPL-3.0. The Aetheris core and author credit may not be removed.
