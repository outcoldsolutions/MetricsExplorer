#!/usr/bin/env python3
"""Checks that a release tag matches the version everywhere the app records it.

  - the tag is vX.Y.Z;
  - app.conf [launcher] version and [id] version are X.Y.Z;
  - app.manifest info.id.version is X.Y.Z;
  - the newest ## heading in RELEASE-NOTES.md is X.Y.Z, with notes under it;
  - app.conf [install] build and app.manifest releaseDate went up since the previous tag.

With --notes-out, also writes that version's RELEASE-NOTES.md section to a file.
Usage: scripts/check_release.py vX.Y.Z [--notes-out PATH]
"""

import argparse
import configparser
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git(*args):
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout


def read_conf(text):
    parser = configparser.ConfigParser(interpolation=None)
    parser.optionxform = str
    parser.read_string(text)
    return parser


def release_notes(text, version):
    """Returns (newest heading, section text for version or None)."""
    headings = list(re.finditer(r"^## +(.+?)\s*$", text, re.M))
    newest = headings[0].group(1) if headings else None
    for i, h in enumerate(headings):
        if h.group(1) == version:
            end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
            return newest, text[h.end():end].strip()
    return newest, None


def previous_tag(tag):
    try:
        return git("describe", "--tags", "--abbrev=0", "--match", "v*", f"{tag}^").strip()
    except subprocess.CalledProcessError:
        return None  # first release


def main():
    args = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    args.add_argument("tag")
    args.add_argument("--notes-out", type=Path)
    args = args.parse_args()

    errors = []
    match = re.fullmatch(r"v(\d+\.\d+\.\d+)", args.tag)
    if not match:
        print(f"::error::Tag {args.tag} is not vX.Y.Z")
        return 1
    version = match.group(1)

    conf = read_conf((ROOT / "default" / "app.conf").read_text(encoding="utf-8"))
    for stanza in ("launcher", "id"):
        found = conf.get(stanza, "version", fallback=None)
        if found != version:
            errors.append(f"app.conf [{stanza}] version is {found}, tag is {version}")

    manifest = json.loads((ROOT / "app.manifest").read_text(encoding="utf-8"))
    found = manifest["info"]["id"]["version"]
    if found != version:
        errors.append(f"app.manifest info.id.version is {found}, tag is {version}")

    newest, notes = release_notes((ROOT / "RELEASE-NOTES.md").read_text(encoding="utf-8"), version)
    if newest != version:
        errors.append(f"newest RELEASE-NOTES.md heading is {newest}, tag is {version}")
    if not notes:
        errors.append(f"RELEASE-NOTES.md has no notes under ## {version}")

    build = conf.get("install", "build", fallback="")
    release_date = manifest["info"].get("releaseDate") or ""
    if not build.isdigit():
        errors.append(f"app.conf [install] build {build!r} is not a number")
    try:
        datetime.date.fromisoformat(release_date)
    except ValueError:
        errors.append(f"app.manifest releaseDate {release_date!r} is not YYYY-MM-DD")

    prev = previous_tag(args.tag)
    if prev and not errors:
        prev_build = read_conf(git("show", f"{prev}:default/app.conf")).get("install", "build")
        prev_date = json.loads(git("show", f"{prev}:app.manifest"))["info"].get("releaseDate") or ""
        if int(build) <= int(prev_build):
            errors.append(f"app.conf [install] build {build} is not above {prev_build} from {prev}")
        if release_date <= prev_date:
            errors.append(f"app.manifest releaseDate {release_date} is not after {prev_date} from {prev}")

    for e in errors:
        print(f"::error::{e}")
    if errors:
        return 1

    print(f"{args.tag}: versions agree" + (f"; build and releaseDate bumped since {prev}" if prev else ""))
    if args.notes_out:
        args.notes_out.write_text(notes + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
