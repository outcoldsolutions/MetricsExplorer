#!/usr/bin/env python3
"""Prints the summary and every non-passing check from an AppInspect JSON report.

Failures and errors become GitHub error annotations; warnings and future failures
become warning annotations. Pass or fail is left to AppInspect's exit code.
Usage: scripts/appinspect_summary.py REPORT.json
"""

import json
import sys

LEVELS = {"failure": "error", "error": "error", "future_failure": "warning", "warning": "warning"}


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        report = json.load(f)

    print("AppInspect summary: " + ", ".join(f"{k} {v}" for k, v in report["summary"].items()))
    for app in report["reports"]:
        for group in app["groups"]:
            for check in group["checks"]:
                level = LEVELS.get(check["result"])
                if not level:
                    continue
                messages = [m["message"] for m in check["messages"]] or [check["description"]]
                for message in messages:
                    # Annotations are one line each; keep the full text in the log.
                    print(f"::{level} title=AppInspect {check['result']}: {check['name']}::{message.splitlines()[0]}")
                    print(f"  {check['result']}: {check['name']}: {message}")


if __name__ == "__main__":
    main()
