<div align="center">

<img src="docs/logo.png" alt="SessionHop" width="148">

# SessionHop

### Hop your Patreon session into Cursor.

Copy your login from Firefox, Chrome, Vivaldi, or Tor Browser — one command, no broken Google popups.

<sub><code>patreon-cursor-session-sync</code> on GitHub · <strong>English</strong> · <a href="README.de.md">Deutsch</a></sub>

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-0d1117?style=for-the-badge&labelColor=F96854)](LICENSE)
[![Linux](https://img.shields.io/badge/Linux-only-0d1117?style=for-the-badge&labelColor=30363d)]()
[![Python](https://img.shields.io/badge/Python-3.9+-0d1117?style=for-the-badge&logo=python&logoColor=white&labelColor=3776AB)]()
[![stdlib](https://img.shields.io/badge/deps-stdlib_only-0d1117?style=for-the-badge&labelColor=238636)]()

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

**SessionHop** copies your Patreon `session_id` and cookies into Cursor’s browser — you open Patreon **already logged in**.

> Unofficial · Linux only · Patreon only · transfers sessions, does not fix OAuth.

---

## Quick start

```bash
git clone https://github.com/benjarogit/patreon-cursor-session-sync.git
cd patreon-cursor-session-sync
chmod +x sessionhop.py

# 1. Log into Patreon in Firefox or Chrome
# 2. Hop the session
./sessionhop.py

# 3. Open in Cursor → https://www.patreon.com/home
```

<details>
<summary><strong>Install as <code>sessionhop</code> command</strong></summary>

```bash
ln -s "$(pwd)/sessionhop.py" ~/.local/bin/sessionhop
sessionhop
```

</details>

---

## Commands

| | |
|:---|:---|
| `./sessionhop.py` | Auto-pick best profile |
| `./sessionhop.py --list` | Show all detected profiles |
| `./sessionhop.py --from firefox` | Firefox |
| `./sessionhop.py --from vivaldi` | Vivaldi |
| `./sessionhop.py --from tor-browser` | Tor Browser |
| `./sessionhop.py --from chrome --profile "Profile 1"` | Specific profile |

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

Safari (macOS) · Windows / macOS paths

</details>

---

## How it works

```
   ┌─────────────┐                              ┌─────────────┐
   │  Browser    │   session_id + cookies       │   Cursor    │
   │  (source)   │ ─────── SessionHop ────────► │   browser   │
   └─────────────┘   SQLite · SIGHUP reload   └─────────────┘
```

1. Read Patreon cookies from source profile  
2. Write to `~/.config/Cursor/Partitions/cursor-browser/Cookies`  
3. Reload Cursor’s cookie jar  
4. Backup previous DB (timestamped)  

---

## Limits

- Session expires when Patreon logs you out — hop again  
- Patreon only (not Ko-fi, GitHub, …)  
- Source DB may be locked while browser runs  

---

<div align="center">

<br>

**[MIT License](LICENSE)** · [benjarogit](https://github.com/benjarogit)

<sub>SessionHop — unofficial, not affiliated with Patreon or Cursor.</sub>

</div>
