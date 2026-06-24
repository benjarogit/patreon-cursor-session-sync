<div align="center">

<img src="docs/logo.png" alt="patreon-cursor-session-sync" width="160">

# patreon-cursor-session-sync

### Patreon in Cursor — direkt eingeloggt.

Session aus Firefox, Chrome, Vivaldi oder Tor Browser in den Cursor-Browser übernehmen.  
Ein Befehl. Keine kaputten Google-Popups.

**Deutsch** · [English](README.md)

<br>

[![License: MIT](https://img.shields.io/badge/Lizenz-MIT-2d2d2d?style=for-the-badge&labelColor=F96854)](LICENSE)
[![Linux](https://img.shields.io/badge/nur-Linux-2d2d2d?style=for-the-badge&labelColor=555)]()
[![Python](https://img.shields.io/badge/Python-3.9+-2d2d2d?style=for-the-badge&logo=python&logoColor=white&labelColor=3776AB)]()
[![stdlib](https://img.shields.io/badge/Abhängigkeiten-nur_stdlib-2d2d2d?style=for-the-badge&labelColor=2ea043)]()

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

Dieses Tool **schließt die Lücke** — es kopiert `session_id` und zugehörige Cookies nach Cursor.

> Inoffizielles Hilfswerkzeug · nur Linux · nur Patreon · kein OAuth-Fix, sondern Session-Transfer.

---

## Schnellstart

```bash
git clone https://github.com/benjarogit/patreon-cursor-session-sync.git
cd patreon-cursor-session-sync
chmod +x sync-patreon-cursor-session.py

# 1. In Firefox oder Chrome bei Patreon einloggen
# 2. Sync starten
./sync-patreon-cursor-session.py

# 3. In Cursor öffnen
# → https://www.patreon.com/home
```

<details>
<summary><strong>Optional: als <code>patreon-cursor-sync</code> installieren</strong></summary>

```bash
ln -s "$(pwd)/sync-patreon-cursor-session.py" ~/.local/bin/patreon-cursor-sync
patreon-cursor-sync
```

</details>

---

## Befehle

| | |
|:---|:---|
| `./sync-patreon-cursor-session.py` | Bestes Profil automatisch wählen |
| `./sync-patreon-cursor-session.py --list` | Alle erkannten Profile |
| `./sync-patreon-cursor-session.py --from firefox` | Firefox |
| `./sync-patreon-cursor-session.py --from vivaldi` | Vivaldi |
| `./sync-patreon-cursor-session.py --from tor-browser` | Tor Browser |
| `./sync-patreon-cursor-session.py --from chrome --profile "Profile 1"` | Bestimmtes Profil |

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

Verschlüsselte Cookies (Keyring)? Quellbrowser schließen oder Firefox nutzen.

</details>

<details>
<summary><strong>Nicht unterstützt</strong></summary>

<br>

Safari (macOS, eigenes Format) · Windows / macOS Pfade

</details>

---

## Funktionsweise

```
   ┌─────────────┐                              ┌─────────────┐
   │  Browser    │   session_id + Cookies       │   Cursor    │
   │  (Quelle)   │ ─────────────────────────► │   Browser   │
   └─────────────┘   SQLite · SIGHUP reload   └─────────────┘
```

1. Patreon-Cookies aus Quellprofil lesen  
2. Schreiben nach `~/.config/Cursor/Partitions/cursor-browser/Cookies`  
3. Cookie-Cache in Cursor neu laden  
4. Backup der alten DB (mit Zeitstempel)  

---

## Grenzen

- Session endet bei Logout — erneut syncen  
- Nur Patreon (nicht Ko-fi, GitHub, …)  
- Cookie-DB kann bei laufendem Browser gesperrt sein  

---

<div align="center">

<br>

**[MIT-Lizenz](LICENSE)** · [benjarogit](https://github.com/benjarogit)

<sub>Inoffizielles Tool — nicht mit Patreon oder Cursor verbunden.</sub>

</div>
