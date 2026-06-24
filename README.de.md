<div align="center">

<img src="docs/logo.png" alt="SessionHop" width="148">

# SessionHop

### Patreon-Session in Cursor — ein Hop, fertig.

Login aus Firefox, Chrome, Vivaldi oder Tor Browser übernehmen — ein Befehl, keine kaputten Google-Popups.

<sub><code>patreon-cursor-session-sync</code> auf GitHub · <strong>Deutsch</strong> · <a href="README.md">English</a></sub>

<br>

[![License: MIT](https://img.shields.io/badge/Lizenz-MIT-0d1117?style=for-the-badge&labelColor=F96854)](LICENSE)
[![Linux](https://img.shields.io/badge/nur-Linux-0d1117?style=for-the-badge&labelColor=30363d)]()
[![Python](https://img.shields.io/badge/Python-3.9+-0d1117?style=for-the-badge&logo=python&logoColor=white&labelColor=3776AB)]()
[![stdlib](https://img.shields.io/badge/Abhängigkeiten-nur_stdlib-0d1117?style=for-the-badge&labelColor=238636)]()

<br>

[Schnellstart](#-schnellstart) · [Browser](#-browser) · [Funktionsweise](#-funktionsweise)

</div>

<br>

---

## Warum es das gibt

<table>
<tr>
<td width="50%" valign="top">

**In Cursor**

- Google-Login → leere Tabs  
- Popups ohne Rückverbindung  
- FedCM / Cookie-Probleme  

</td>
<td width="50%" valign="top">

**In Firefox / Chrome**

- Login funktioniert  
- Session ist schon da  

</td>
</tr>
</table>

**SessionHop** kopiert `session_id` und Cookies in den Cursor-Browser — Patreon öffnet sich **direkt eingeloggt**.

> Inoffiziell · nur Linux · nur Patreon · Session-Transfer, kein OAuth-Fix.

---

## Schnellstart

```bash
git clone https://github.com/benjarogit/patreon-cursor-session-sync.git
cd patreon-cursor-session-sync
chmod +x sessionhop.py

# 1. In Firefox oder Chrome bei Patreon einloggen
# 2. Session hoppen
./sessionhop.py

# 3. In Cursor → https://www.patreon.com/home
```

<details>
<summary><strong>Als <code>sessionhop</code>-Befehl installieren</strong></summary>

```bash
ln -s "$(pwd)/sessionhop.py" ~/.local/bin/sessionhop
sessionhop
```

</details>

---

## Befehle

| | |
|:---|:---|
| `./sessionhop.py` | Bestes Profil automatisch |
| `./sessionhop.py --list` | Alle erkannten Profile |
| `./sessionhop.py --from firefox` | Firefox |
| `./sessionhop.py --from vivaldi` | Vivaldi |
| `./sessionhop.py --from tor-browser` | Tor Browser |
| `./sessionhop.py --from chrome --profile "Profile 1"` | Bestimmtes Profil |

Noch ausgeloggt? **Developer → Reload Window**, dann Patreon erneut öffnen.

---

## Browser

<details open>
<summary><strong>Gecko</strong> <code>cookies.sqlite</code></summary>

<br>

`firefox` · `waterfox` · `librewolf` · `tor-browser` · `pale-moon` · `floorp` · `zen` · `basilisk`

| Browser | Pfad |
|:--------|:-----|
| Firefox | `~/.mozilla/firefox/<profil>/` |
| Waterfox | `~/.waterfox/` |
| LibreWolf | `~/.librewolf/` |
| Tor Browser | `~/.local/share/torbrowser/.../Browser/` |

</details>

<details>
<summary><strong>Chromium</strong> <code>Cookies</code></summary>

<br>

`chrome` · `chromium` · `vivaldi` · `brave` · `edge` · `opera` · `sidekick` · `yandex` · `iridium`

| Browser | Pfad |
|:--------|:-----|
| Chrome | `~/.config/google-chrome/` |
| Vivaldi | `~/.config/vivaldi/` |
| Brave | `~/.config/BraveSoftware/Brave-Browser/` |
| Edge | `~/.config/microsoft-edge/` |

Verschlüsselte Cookies? Quellbrowser schließen oder Firefox nutzen.

</details>

<details>
<summary><strong>Nicht unterstützt</strong></summary>

<br>

Safari (macOS) · Windows / macOS Pfade

</details>

---

## Funktionsweise

```
   ┌─────────────┐                              ┌─────────────┐
   │  Browser    │   session_id + Cookies       │   Cursor    │
   │  (Quelle)   │ ─────── SessionHop ────────► │   Browser   │
   └─────────────┘   SQLite · SIGHUP reload   └─────────────┘
```

1. Patreon-Cookies aus Quellprofil lesen  
2. Schreiben nach `~/.config/Cursor/Partitions/cursor-browser/Cookies`  
3. Cookie-Cache neu laden  
4. Backup der alten DB  

---

## Grenzen

- Session endet bei Logout — erneut hoppen  
- Nur Patreon  
- Cookie-DB kann bei laufendem Browser gesperrt sein  

---

<div align="center">

<br>

**[MIT-Lizenz](LICENSE)** · [benjarogit](https://github.com/benjarogit)

<sub>SessionHop — inoffiziell, nicht mit Patreon oder Cursor verbunden.</sub>

</div>
