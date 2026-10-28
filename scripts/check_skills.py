#!/usr/bin/env python3
"""Fail if any skill's SKILL.md has no description, one over claude.ai's 1,024-character limit, or one
with < or > (claude.ai rejects XML tags in a description).

Standard library only. Reads the YAML frontmatter forms the skills use: a plain or quoted
one-line value (with indented continuation lines) or a > / | block scalar.
"""
import sys
from pathlib import Path

LIMIT = 1024
ROOT = Path(__file__).resolve().parent.parent


def frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            return lines[1:i]
    return None


def description(fm):
    for i, line in enumerate(fm):
        if not line.startswith("description:"):
            continue
        value = line[len("description:"):].strip()
        rest = []
        for more in fm[i + 1:]:
            if more and not more[0].isspace():
                break
            rest.append(more.strip())
        if value[:1] in (">", "|"):
            joiner = " " if value[0] == ">" else "\n"
            return joiner.join(r for r in rest if r).strip()
        value = " ".join([value] + [r for r in rest if r])
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            quote, value = value[0], value[1:-1]
            value = value.replace("''", "'") if quote == "'" else value.replace('\\"', '"')
        return value
    return None


def main():
    failed = False
    for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
        name = skill.parent.name
        fm = frontmatter(skill.read_text(encoding="utf-8"))
        desc = description(fm) if fm else None
        if not desc:
            print(f"FAIL {name}: no description in the frontmatter")
            failed = True
        elif len(desc) > LIMIT:
            print(f"FAIL {name}: description is {len(desc)} characters (limit {LIMIT})")
            failed = True
        elif "<" in desc or ">" in desc:
            print(f"FAIL {name}: description contains < or > (claude.ai rejects XML tags); write PROJECT, not <project>")
            failed = True
        else:
            print(f"ok   {name}: {len(desc)} characters")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
