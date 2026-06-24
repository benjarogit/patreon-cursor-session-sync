#!/usr/bin/env python3
"""SessionHop — Patreon-Session aus einem Systembrowser in den Cursor-Browser (Linux)."""
from __future__ import annotations

import argparse
import glob
import hashlib
import shutil
import sqlite3
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

CUR_PART = Path.home() / ".config/Cursor/Partitions/cursor-browser"
CUR_COOKIES = CUR_PART / "Cookies"
CHROME_EPOCH_OFFSET = 11644473600

# Gecko: cookies.sqlite + profiles.ini (Firefox, Waterfox, Tor Browser, …)
GECKO_BROWSERS: dict[str, list[Path]] = {
    "firefox": [Path.home() / ".mozilla/firefox"],
    "waterfox": [
        Path.home() / ".waterfox",
        Path.home() / ".var/app/net.waterfox.waterfox/.waterfox",
        Path.home() / ".var/app/org.waterfox.waterfox/.waterfox",
    ],
    "librewolf": [Path.home() / ".librewolf"],
    "tor-browser": [
        Path.home() / ".local/share/torbrowser",
        Path.home() / ".tb",
        Path.home() / "tor-browser",
        Path.home() / ".tor browser",
    ],
    "pale-moon": [Path.home() / ".moonchild productions/pale moon"],
    "basilisk": [Path.home() / ".basilisk"],
    "floorp": [Path.home() / ".floorp"],
    "zen": [Path.home() / ".zen"],
    "thunderbird": [Path.home() / ".thunderbird"],  # same engine; rarely Patreon
}

# Chromium: Cookies SQLite (Chrome, Vivaldi, Edge, …)
CHROMIUM_BROWSERS: dict[str, Path] = {
    "chrome": Path.home() / ".config/google-chrome",
    "chromium": Path.home() / ".config/chromium",
    "vivaldi": Path.home() / ".config/vivaldi",
    "brave": Path.home() / ".config/BraveSoftware/Brave-Browser",
    "edge": Path.home() / ".config/microsoft-edge",
    "opera": Path.home() / ".config/opera",
    "sidekick": Path.home() / ".config/sidekick-browser",
    "yandex": Path.home() / ".config/yandex-browser",
    "iridium": Path.home() / ".config/iridium",
}

ALL_BROWSER_NAMES = ["auto", *sorted(GECKO_BROWSERS), *sorted(CHROMIUM_BROWSERS)]


@dataclass(frozen=True)
class PatreonCookie:
    name: str
    value: str
    host: str
    path: str
    expires_utc: int
    secure: int
    httponly: int
    samesite: int


def chrome_now() -> int:
    return int((time.time() + CHROME_EPOCH_OFFSET) * 1_000_000)


def ff_expiry_to_chrome(expiry_ms: int) -> int:
    return int((expiry_ms / 1000 + CHROME_EPOCH_OFFSET) * 1_000_000)


def ff_samesite(ss: int) -> int:
    return {0: -1, 1: 1, 2: 2, 256: -1}.get(ss, -1)


def _skip_profile_path(path: Path) -> bool:
    text = str(path)
    blocked = (".bak", "Crash Reports", "Pending Pings", ".Trash", "/Trash/")
    return any(part in text for part in blocked)


def gecko_cookie_dbs(roots: list[Path]) -> list[Path]:
    dbs: list[Path] = []
    seen: set[Path] = set()

    for root in roots:
        if not root.is_dir():
            continue
        profiles_ini = root / "profiles.ini"
        if profiles_ini.is_file():
            for line in profiles_ini.read_text(encoding="utf-8", errors="ignore").splitlines():
                if not line.startswith("Path="):
                    continue
                rel = line.split("=", 1)[1].strip()
                if _skip_profile_path(Path(rel)):
                    continue
                db = root / rel / "cookies.sqlite"
                if db.is_file() and db not in seen:
                    seen.add(db)
                    dbs.append(db)
        for db in root.glob("**/cookies.sqlite"):
            if _skip_profile_path(db) or db in seen:
                continue
            seen.add(db)
            dbs.append(db)
    return sorted(dbs)


def chromium_cookie_dbs(config_dir: Path) -> list[Path]:
    if not config_dir.is_dir():
        return []
    dbs: list[Path] = []
    for pattern in ("Default/Cookies", "Profile */Cookies", "Guest Profile/Cookies"):
        dbs.extend(Path(p) for p in glob.glob(str(config_dir / pattern)))
    return sorted({db for db in dbs if db.is_file()})


def discover_sources() -> list[tuple[str, Path]]:
    sources: list[tuple[str, Path]] = []
    for browser, roots in GECKO_BROWSERS.items():
        for db in gecko_cookie_dbs(roots):
            profile = db.parent.name
            sources.append((f"{browser}:{profile}", db))
    for browser, config_dir in CHROMIUM_BROWSERS.items():
        for db in chromium_cookie_dbs(config_dir):
            sources.append((f"{browser}:{db.parent.name}", db))
    return sources


def snapshot_db(db_path: Path) -> Path:
    digest = hashlib.sha1(str(db_path).encode()).hexdigest()[:10]
    tmp = Path(f"/tmp/patreon-cursor-session-{digest}.sqlite")
    shutil.copy2(db_path, tmp)
    return tmp


def read_gecko_patreon_cookies(db_path: Path) -> list[PatreonCookie]:
    snap = snapshot_db(db_path)
    con = sqlite3.connect(f"file:{snap}?mode=ro", uri=True)
    rows = con.execute(
        """
        SELECT name, value, host, path, expiry, isSecure, isHttpOnly, sameSite
        FROM moz_cookies
        WHERE host LIKE '%patreon%' AND expiry > ?
        """,
        (int(time.time() * 1000),),
    ).fetchall()
    con.close()

    best: dict[tuple[str, str, str], tuple] = {}
    for row in rows:
        key = (row[2], row[0], row[3])
        if key not in best or row[4] > best[key][4]:
            best[key] = row

    return [
        PatreonCookie(
            name=name,
            value=value,
            host=host,
            path=path,
            expires_utc=ff_expiry_to_chrome(expiry),
            secure=secure,
            httponly=httponly,
            samesite=ff_samesite(samesite),
        )
        for name, value, host, path, expiry, secure, httponly, samesite in best.values()
    ]


def read_chromium_patreon_cookies(db_path: Path) -> list[PatreonCookie]:
    snap = snapshot_db(db_path)
    con = sqlite3.connect(f"file:{snap}?mode=ro", uri=True)
    rows = con.execute(
        """
        SELECT name, value, length(encrypted_value), host_key, path,
               expires_utc, is_secure, is_httponly, samesite
        FROM cookies
        WHERE host_key LIKE '%patreon%' AND expires_utc > ?
        """,
        (chrome_now(),),
    ).fetchall()
    con.close()

    best: dict[tuple[str, str, str], tuple] = {}
    for row in rows:
        key = (row[3], row[0], row[4])
        if key not in best or row[5] > best[key][5]:
            best[key] = row

    cookies: list[PatreonCookie] = []
    for name, value, enc_len, host, path, expires, secure, httponly, samesite in best.values():
        if not value and enc_len:
            raise ValueError(
                f"Cookie '{name}' ist verschlüsselt (Keyring). "
                "Browser schließen oder anderen Browser/Profil wählen."
            )
        cookies.append(
            PatreonCookie(
                name=name,
                value=value,
                host=host,
                path=path,
                expires_utc=expires,
                secure=secure,
                httponly=httponly,
                samesite=samesite,
            )
        )
    return cookies


def is_gecko_db(db_path: Path) -> bool:
    return db_path.name == "cookies.sqlite"


def read_patreon_cookies(source_label: str, db_path: Path) -> list[PatreonCookie]:
    if is_gecko_db(db_path):
        return read_gecko_patreon_cookies(db_path)
    return read_chromium_patreon_cookies(db_path)


def pick_best_session_source(
    dbs: list[tuple[str, Path]],
) -> tuple[str, Path] | None:
    best: tuple[str, Path, int] | None = None
    for label, db in dbs:
        try:
            cookies = read_patreon_cookies(label, db)
        except (sqlite3.Error, ValueError):
            continue
        session = next((c for c in cookies if c.name == "session_id" and c.value), None)
        if not session:
            continue
        if best is None or session.expires_utc > best[2]:
            best = (label, db, session.expires_utc)
    if best is None:
        return None
    return best[0], best[1]


def labeled_gecko_sources(browser: str, profile: str | None) -> list[tuple[str, Path]]:
    roots = GECKO_BROWSERS.get(browser, [])
    dbs = gecko_cookie_dbs(roots)
    if profile:
        dbs = [db for db in dbs if db.parent.name == profile]
    return [(f"{browser}:{db.parent.name}", db) for db in dbs]


def resolve_source(browser: str, profile: str | None) -> tuple[str, Path]:
    browser = browser.lower()

    if browser == "auto":
        picked = pick_best_session_source(discover_sources())
        if not picked:
            raise SystemExit(
                "Keine lesbare Patreon session_id gefunden. "
                "In einem unterstützten Browser bei Patreon einloggen."
            )
        label, db = picked
        print(f"Quelle automatisch gewählt: {label}")
        return label, db

    if browser in GECKO_BROWSERS:
        labeled = labeled_gecko_sources(browser, profile)
        if not labeled:
            raise SystemExit(f"Kein Gecko-Profil für '{browser}' gefunden.")
        picked = pick_best_session_source(labeled)
        if not picked:
            raise SystemExit(f"Keine gültige Patreon session_id für '{browser}' gefunden.")
        return picked

    if browser in CHROMIUM_BROWSERS:
        dbs = chromium_cookie_dbs(CHROMIUM_BROWSERS[browser])
        if profile:
            dbs = [db for db in dbs if db.parent.name == profile]
        if not dbs:
            raise SystemExit(f"Kein Cookie-Store für '{browser}' gefunden.")
        labeled = [(f"{browser}:{db.parent.name}", db) for db in dbs]
        picked = pick_best_session_source(labeled)
        if not picked:
            raise SystemExit(f"Keine gültige Patreon session_id für '{browser}' gefunden.")
        return picked

    raise SystemExit(f"Unbekannter Browser '{browser}'. --list oder: {', '.join(ALL_BROWSER_NAMES)}")


def upsert_patreon_cookies(cur_db: Path, cookies: list[PatreonCookie]) -> None:
    now = chrome_now()
    con = sqlite3.connect(cur_db)
    for cookie in cookies:
        for hca in (0, 1):
            con.execute(
                """
                INSERT INTO cookies (
                    creation_utc, host_key, top_frame_site_key, name, value, encrypted_value,
                    path, expires_utc, is_secure, is_httponly, last_access_utc,
                    has_expires, is_persistent, priority, samesite, source_scheme, source_port,
                    last_update_utc, source_type, has_cross_site_ancestor
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(host_key, top_frame_site_key, has_cross_site_ancestor, name, path, source_scheme, source_port)
                DO UPDATE SET
                    value=excluded.value,
                    expires_utc=excluded.expires_utc,
                    is_secure=excluded.is_secure,
                    is_httponly=excluded.is_httponly,
                    samesite=excluded.samesite,
                    last_update_utc=excluded.last_update_utc
                """,
                (
                    now,
                    cookie.host,
                    "",
                    cookie.name,
                    cookie.value,
                    b"",
                    cookie.path,
                    cookie.expires_utc,
                    cookie.secure,
                    cookie.httponly,
                    now,
                    1,
                    1,
                    1,
                    cookie.samesite,
                    2,
                    443,
                    now,
                    2,
                    hca,
                ),
            )
    con.commit()
    con.close()


def reload_cursor_cookie_jar() -> bool:
    out = subprocess.run(
        ["pgrep", "-f", r"network.mojom.NetworkService.*user-data-dir=.*/.config/Cursor"],
        capture_output=True,
        text=True,
        check=False,
    )
    pid = out.stdout.strip().split("\n", 1)[0] if out.stdout.strip() else ""
    if not pid:
        return False
    subprocess.run(["kill", "-HUP", pid], check=False)
    return True


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SessionHop — Patreon-Session in den Cursor-Browser übernehmen.",
    )
    parser.add_argument(
        "--from",
        dest="browser",
        default="auto",
        metavar="BROWSER",
        help=f"Quellbrowser: {', '.join(ALL_BROWSER_NAMES)}",
    )
    parser.add_argument(
        "--profile",
        help="Profilname, z. B. Default oder hauptprofil (optional)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Gefundene Browser-Profile anzeigen und beenden",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    if args.list:
        for label, db in discover_sources():
            print(f"{label}\t{db}")
        return 0

    if not CUR_COOKIES.exists():
        raise SystemExit(f"Cursor-Browser-Cookies nicht gefunden: {CUR_COOKIES}")

    label, source_db = resolve_source(args.browser, args.profile)
    cookies = read_patreon_cookies(label, source_db)

    if not any(c.name == "session_id" and c.value for c in cookies):
        raise SystemExit(f"Keine gültige Patreon session_id in {label} gefunden.")

    backup = CUR_PART / f"Cookies.bak.{int(time.time())}"
    shutil.copy2(CUR_COOKIES, backup)
    upsert_patreon_cookies(CUR_COOKIES, cookies)
    reloaded = reload_cursor_cookie_jar()

    print(f"OK: {len(cookies)} Patreon-Cookies von {label} übernommen")
    print(f"Backup: {backup}")
    if reloaded:
        print("Cookie-Jar neu geladen. Patreon-Tab öffnen: https://www.patreon.com/home")
    else:
        print("Hinweis: Cursor-Fenster einmal neu laden (Reload Window), dann Patreon öffnen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
