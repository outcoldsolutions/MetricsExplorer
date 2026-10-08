#!/usr/bin/env python3
"""Checks that the app's config, manifest, nav and dashboard files parse.

Dashboard Studio views (version="2") also have their JSON definition parsed.
Run from anywhere: scripts/validate.py
"""

import configparser
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def check_conf(path):
    parser = configparser.ConfigParser(interpolation=None, strict=True)
    parser.optionxform = str
    parser.SECTCRE = re.compile(r"\[(?P<header>.*)\]")  # .meta files use an empty [] stanza
    with path.open(encoding="utf-8") as f:
        # Splunk allows settings before the first stanza; give them a section.
        parser.read_string("[__top__]\n" + f.read(), source=str(path))


def check_xml(path):
    root = ET.parse(path).getroot()
    if root.tag == "dashboard" and root.get("version") == "2":
        definition = root.find("definition")
        if definition is None or not (definition.text or "").strip():
            raise ValueError("Dashboard Studio view has no <definition>")
        json.loads(definition.text)


def main():
    checks = [(p, check_conf) for p in sorted((ROOT / "default").glob("*.conf"))]
    checks += [(p, check_conf) for p in sorted((ROOT / "metadata").glob("*.meta"))]
    checks += [(p, check_xml) for p in sorted((ROOT / "default" / "data" / "ui").rglob("*.xml"))]
    checks.append((ROOT / "app.manifest", lambda p: json.loads(p.read_text(encoding="utf-8"))))

    failed = False
    for path, check in checks:
        name = path.relative_to(ROOT)
        try:
            check(path)
            print(f"ok    {name}")
        except Exception as e:  # report every bad file, not just the first
            failed = True
            print(f"FAIL  {name}: {e}")
            print(f"::error file={name}::{e}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
