# patreon-cursor-session-sync

**English** · [Deutsch](README.de.md)

Sync your Patreon login session from a system browser into the [Cursor IDE](https://cursor.com) embedded browser on Linux.

Patreon’s Google sign-in often fails inside Cursor (blank Google tabs, broken popups, FedCM issues). If you are already logged into Patreon in Firefox or a Chromium-based browser, this tool copies the session cookies into Cursor so you can use Patreon without re-authenticating.

> **Scope:** Linux only · Patreon only · Cursor embedded browser as target · not an official Cursor or Patreon product.

---

## Requirements

- Linux
- [Cursor IDE](https://cursor.com) with the built-in browser
- Logged into Patreon in at least one supported source browser

**Dependencies:** Python 3.9+ (stdlib only, no pip packages)

---

## Supported source browsers (Linux)

### Gecko (`cookies.sqlite`)

| `--from` | Typical profile path |
|----------|----------------------|
| `firefox` | `~/.mozilla/firefox/<profile>/` |
| `waterfox` | `~/.waterfox/`, Flatpak `~/.var/app/.../waterfox/` |
| `librewolf` | `~/.librewolf/` |
| `tor-browser` | `~/.local/share/torbrowser/.../TorBrowser/Data/Browser/` |
| `pale-moon` | `~/.moonchild productions/pale moon/` |
| `floorp`, `zen`, `basilisk` | `~/.floorp/`, `~/.zen/`, `~/.basilisk/` |

Tor Browser is **Firefox-based (Gecko)**, not Chromium.

### Chromium (`Cookies`)

| `--from` | Config path |
|----------|-------------|
| `chrome` | `~/.config/google-chrome/` |
| `chromium` | `~/.config/chromium/` |
| `vivaldi` | `~/.config/vivaldi/` |
| `brave` | `~/.config/BraveSoftware/Brave-Browser/` |
| `edge` | `~/.config/microsoft-edge/` |
| `opera`, `sidekick`, `yandex`, `iridium` | respective `~/.config/...` dirs |

Chromium forks share the same cookie schema; only paths differ. Use `--list` to see detected profiles.

### Not supported

| Browser | Reason |
|---------|--------|
| **Safari** | macOS only, proprietary cookie format (not SQLite) |
| **Windows / macOS paths** | This tool targets Linux home-directory layouts only |

### Encrypted cookies

Some Chromium profiles store values in `encrypted_value` (OS keyring). This tool requires readable plaintext `value` fields. If sync fails with an encryption error, close the source browser and retry, or use Firefox as the source.

---

## Installation

```bash
git clone https://github.com/benjarogit/patreon-cursor-session-sync.git
cd patreon-cursor-session-sync
chmod +x sync-patreon-cursor-session.py
```

Optional: add to `PATH` or symlink:

```bash
ln -s "$(pwd)/sync-patreon-cursor-session.py" ~/.local/bin/patreon-cursor-sync
```

---

## Usage

### Automatic (recommended)

Finds the first source profile with a valid Patreon `session_id`:

```bash
./sync-patreon-cursor-session.py
# or explicitly:
./sync-patreon-cursor-session.py --from auto
```

### Specific browser

```bash
./sync-patreon-cursor-session.py --from firefox
./sync-patreon-cursor-session.py --from vivaldi
./sync-patreon-cursor-session.py --from chrome --profile "Profile 1"
```

### List detected profiles

```bash
./sync-patreon-cursor-session.py --list
```

### After sync

1. Open `https://www.patreon.com/home` in Cursor’s browser, or refresh an existing Patreon tab.
2. If still logged out: **Command Palette → Developer: Reload Window**, then open Patreon again.

---

## How it works

```
┌─────────────────┐     copy Patreon cookies      ┌──────────────────────┐
│ Firefox /       │ ────────────────────────────► │ Cursor browser       │
│ Chrome / Vivaldi│     into SQLite cookie DB     │ (cursor-browser      │
│ (logged in)     │     + reload cookie jar       │  partition)          │
└─────────────────┘                               └──────────────────────┘
```

1. Reads Patreon cookies (`session_id`, etc.) from the source browser profile.
2. Writes them into `~/.config/Cursor/Partitions/cursor-browser/Cookies`.
3. Sends `SIGHUP` to Cursor’s network service so the in-memory cookie jar reloads.
4. Creates a timestamped backup of the previous Cursor cookie database.

---

## Typical profile paths (Linux)

| Browser | Config directory |
|---------|------------------|
| Firefox | `~/.mozilla/firefox/<profile>/cookies.sqlite` |
| Chrome | `~/.config/google-chrome/<profile>/Cookies` |
| Vivaldi | `~/.config/vivaldi/<profile>/Cookies` |
| Brave | `~/.config/BraveSoftware/Brave-Browser/<profile>/Cookies` |
| Edge | `~/.config/microsoft-edge/<profile>/Cookies` |
| Cursor (target) | `~/.config/Cursor/Partitions/cursor-browser/Cookies` |

---

## Limitations

- Session expires when Patreon logs you out or cookies expire — log in again in the source browser and re-run sync.
- Does not fix Google OAuth inside Cursor; it only transfers an existing session.
- Does not sync other sites (Ko-fi, GitHub, etc.).
- Reading cookies from a running browser can fail if the database is locked — close the source browser if needed.

---

## License

MIT — see [LICENSE](LICENSE).
