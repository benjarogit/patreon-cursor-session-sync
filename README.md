<div align="center">

<img src="docs/logo.png" alt="patreon-cursor-session-sync" width="160">

# patreon-cursor-session-sync

### Patreon in Cursor — already logged in.

Copy your session from Firefox, Chrome, Vivaldi, or Tor Browser into Cursor’s embedded browser.  
One command. No broken Google popups.

**English** · [Deutsch](README.de.md)

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-2d2d2d?style=for-the-badge&labelColor=F96854)](LICENSE)
[![Linux](https://img.shields.io/badge/Linux-only-2d2d2d?style=for-the-badge&labelColor=555)]()
[![Python](https://img.shields.io/badge/Python-3.9+-2d2d2d?style=for-the-badge&logo=python&logoColor=white&labelColor=3776AB)]()
[![stdlib](https://img.shields.io/badge/deps-stdlib_only-2d2d2d?style=for-the-badge&labelColor=2ea043)]()

<br>

[Quick start](#-quick-start) · [Browsers](#-browsers) · [How it works](#-how-it-works)

</div>

<br>

---

## Why this exists

<table>
<tr>
<td width="50%" valign="top">

**In Cursor**

- Google sign-in opens blank tabs  
- Popups never connect back  
- FedCM / cookie issues  

</td>
<td width="50%" valign="top">

**In Firefox / Chrome**

- Login works normally  
- Session already there  

</td>
</tr>
</table>

This tool **bridges the gap** — it copies your Patreon `session_id` and related cookies into Cursor.

> Unofficial utility · Linux only · Patreon only · does not fix OAuth — transfers an active session.

---

## Quick start

```bash
git clone https://github.com/benjarogit/patreon-cursor-session-sync.git
cd patreon-cursor-session-sync
chmod +x sync-patreon-cursor-session.py

# 1. Log into Patreon in Firefox or Chrome
# 2. Run sync
./sync-patreon-cursor-session.py

# 3. Open in Cursor
# → https://www.patreon.com/home
```

<details>
<summary><strong>Optional: install as <code>patreon-cursor-sync</code></strong></summary>

```bash
ln -s "$(pwd)/sync-patreon-cursor-session.py" ~/.local/bin/patreon-cursor-sync
patreon-cursor-sync
```

</details>

---

## Commands

| | |
|:---|:---|
| `./sync-patreon-cursor-session.py` | Auto-pick best profile |
| `./sync-patreon-cursor-session.py --list` | Show all detected profiles |
| `./sync-patreon-cursor-session.py --from firefox` | Firefox |
| `./sync-patreon-cursor-session.py --from vivaldi` | Vivaldi |
| `./sync-patreon-cursor-session.py --from tor-browser` | Tor Browser |
| `./sync-patreon-cursor-session.py --from chrome --profile "Profile 1"` | Specific profile |

Still logged out? **Developer → Reload Window**, then open Patreon again.

---

## Browsers

<details open>
<summary><strong>Gecko</strong> <code>cookies.sqlite</code></summary>

<br>

`firefox` · `waterfox` · `librewolf` · `tor-browser` · `pale-moon` · `floorp` · `zen` · `basilisk`

| Browser | Path |
|:--------|:-----|
| Firefox | `~/.mozilla/firefox/<profile>/` |
| Waterfox | `~/.waterfox/` |
| LibreWolf | `~/.librewolf/` |
| Tor Browser | `~/.local/share/torbrowser/.../Browser/` |

</details>

<details>
<summary><strong>Chromium</strong> <code>Cookies</code></summary>

<br>

`chrome` · `chromium` · `vivaldi` · `brave` · `edge` · `opera` · `sidekick` · `yandex` · `iridium`

| Browser | Path |
|:--------|:-----|
| Chrome | `~/.config/google-chrome/` |
| Vivaldi | `~/.config/vivaldi/` |
| Brave | `~/.config/BraveSoftware/Brave-Browser/` |
| Edge | `~/.config/microsoft-edge/` |

Encrypted cookies (OS keyring)? Close the source browser or use Firefox.

</details>

<details>
<summary><strong>Not supported</strong></summary>

<br>

Safari (macOS, proprietary format) · Windows / macOS paths

</details>

---

## How it works

```
   ┌─────────────┐                              ┌─────────────┐
   │  Browser    │   session_id + cookies       │   Cursor    │
   │  (source)   │ ─────────────────────────► │   browser   │
   └─────────────┘   SQLite · SIGHUP reload   └─────────────┘
```

1. Read Patreon cookies from source profile  
2. Write to `~/.config/Cursor/Partitions/cursor-browser/Cookies`  
3. Reload Cursor’s cookie jar  
4. Backup previous DB (timestamped)  

---

## Limits

- Session expires when Patreon logs you out — sync again  
- Patreon only (not Ko-fi, GitHub, …)  
- Source DB may be locked while browser runs  

---

<div align="center">

<br>

**[MIT License](LICENSE)** · [benjarogit](https://github.com/benjarogit)

<sub>Unofficial tool — not affiliated with Patreon or Cursor.</sub>

</div>
