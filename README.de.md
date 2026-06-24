# patreon-cursor-session-sync

**Deutsch** · [English](README.md)

Übernimmt deine Patreon-Anmeldung aus einem Systembrowser in den eingebetteten Browser der [Cursor IDE](https://cursor.com) unter Linux.

Der Google-Login bei Patreon funktioniert in Cursor oft nicht (leere Google-Tabs, kaputte Popups, FedCM-Probleme). Bist du in Firefox oder einem Chromium-Browser bereits bei Patreon eingeloggt, kopiert dieses Tool die Session-Cookies nach Cursor — ohne erneute Anmeldung.

> **Geltungsbereich:** Nur Linux · nur Patreon · Ziel ist immer der Cursor-Browser · kein offizielles Cursor- oder Patreon-Produkt.

---

## Voraussetzungen

- Linux
- [Cursor IDE](https://cursor.com) mit eingebautem Browser
- In mindestens einem unterstützten Quellbrowser bei Patreon eingeloggt

**Abhängigkeiten:** Python 3.9+ (nur Standardbibliothek, kein pip)

---

## Unterstützte Quellbrowser (Linux)

### Gecko (`cookies.sqlite`)

| `--from` | Typischer Profilpfad |
|----------|----------------------|
| `firefox` | `~/.mozilla/firefox/<profil>/` |
| `waterfox` | `~/.waterfox/`, Flatpak `~/.var/app/.../waterfox/` |
| `librewolf` | `~/.librewolf/` |
| `tor-browser` | `~/.local/share/torbrowser/.../TorBrowser/Data/Browser/` |
| `pale-moon` | `~/.moonchild productions/pale moon/` |
| `floorp`, `zen`, `basilisk` | `~/.floorp/`, `~/.zen/`, `~/.basilisk/` |

Tor Browser basiert auf **Firefox (Gecko)** — nicht auf Chromium.

### Chromium (`Cookies`)

| `--from` | Konfigurationspfad |
|----------|-------------------|
| `chrome` | `~/.config/google-chrome/` |
| `chromium` | `~/.config/chromium/` |
| `vivaldi` | `~/.config/vivaldi/` |
| `brave` | `~/.config/BraveSoftware/Brave-Browser/` |
| `edge` | `~/.config/microsoft-edge/` |
| `opera`, `sidekick`, `yandex`, `iridium` | jeweiliges `~/.config/...` |

Chromium-Forks teilen dasselbe Schema. Mit `--list` alle erkannten Profile anzeigen.

### Nicht unterstützt

| Browser | Grund |
|---------|--------|
| **Safari** | nur macOS, eigenes Cookie-Format (kein SQLite) |
| **Windows / macOS** | Tool nutzt Linux-Heimverzeichnis-Pfade |

### Verschlüsselte Cookies

Manche Chromium-Profile speichern Werte in `encrypted_value` (OS-Keyring). Das Tool benötigt lesbare Klartext-Werte in `value`. Bei Verschlüsselungsfehler: Quellbrowser schließen und erneut versuchen, oder Firefox als Quelle nutzen.

---

## Installation

```bash
git clone https://github.com/benjarogit/patreon-cursor-session-sync.git
cd patreon-cursor-session-sync
chmod +x sync-patreon-cursor-session.py
```

Optional in den `PATH` legen:

```bash
ln -s "$(pwd)/sync-patreon-cursor-session.py" ~/.local/bin/patreon-cursor-sync
```

---

## Anleitung

### Automatisch (empfohlen)

Sucht das erste Profil mit gültiger Patreon-`session_id`:

```bash
./sync-patreon-cursor-session.py
# oder explizit:
./sync-patreon-cursor-session.py --from auto
```

### Bestimmter Browser

```bash
./sync-patreon-cursor-session.py --from firefox
./sync-patreon-cursor-session.py --from vivaldi
./sync-patreon-cursor-session.py --from chrome --profile "Profile 1"
```

### Verfügbare Profile anzeigen

```bash
./sync-patreon-cursor-session.py --list
```

### Nach dem Sync

1. In Cursor `https://www.patreon.com/home` öffnen oder bestehenden Patreon-Tab neu laden.
2. Falls noch ausgeloggt: **Befehlspalette → Developer: Reload Window**, dann Patreon erneut öffnen.

---

## Funktionsweise

```
┌─────────────────┐     Patreon-Cookies kopieren    ┌──────────────────────┐
│ Firefox /       │ ──────────────────────────────► │ Cursor-Browser       │
│ Chrome / Vivaldi│     in SQLite-Cookie-DB         │ (Partition           │
│ (eingeloggt)    │     + Cookie-Jar neu laden      │  cursor-browser)     │
└─────────────────┘                                 └──────────────────────┘
```

1. Liest Patreon-Cookies (`session_id` usw.) aus dem Quellbrowser-Profil.
2. Schreibt sie nach `~/.config/Cursor/Partitions/cursor-browser/Cookies`.
3. Lädt den Cookie-Cache von Cursor per `SIGHUP` neu.
4. Erstellt ein Backup der bisherigen Cursor-Cookie-Datenbank.

---

## Typische Profilpfade (Linux)

| Browser | Konfigurationsverzeichnis |
|---------|---------------------------|
| Firefox | `~/.mozilla/firefox/<profil>/cookies.sqlite` |
| Chrome | `~/.config/google-chrome/<profil>/Cookies` |
| Vivaldi | `~/.config/vivaldi/<profil>/Cookies` |
| Brave | `~/.config/BraveSoftware/Brave-Browser/<profil>/Cookies` |
| Edge | `~/.config/microsoft-edge/<profil>/Cookies` |
| Cursor (Ziel) | `~/.config/Cursor/Partitions/cursor-browser/Cookies` |

---

## Grenzen

- Session endet, wenn Patreon dich ausloggt oder Cookies ablaufen — erneut im Quellbrowser einloggen und Sync wiederholen.
- Behebt nicht den Google-OAuth-Flow in Cursor, sondern überträgt nur eine bestehende Session.
- Synchronisiert keine anderen Seiten (Ko-fi, GitHub, …).
- Bei laufendem Quellbrowser kann die Datenbank gesperrt sein — ggf. Browser kurz schließen.

---

## Lizenz

MIT — siehe [LICENSE](LICENSE).
