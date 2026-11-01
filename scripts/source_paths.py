"""Extract complete raw source paths from Markdown frontmatter (requires PyYAML)."""
import argparse
from pathlib import Path
import re
import sys

import yaml


def extract_sources(text):
    """Return (paths, recovered); recovery accepts only plain YAML block lists."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing frontmatter")
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise ValueError("unterminated frontmatter")
    front = "\n".join(lines[1:end])
    recovered = False
    try:
        data = yaml.safe_load(front)
    except yaml.YAMLError:
        match = re.search(r"^sources:[ \t]*(?:#.*)?$", front, re.M)
        if not match:
            raise ValueError("malformed YAML; cannot recover sources block") from None
        block = []
        for line in front[match.end():].splitlines():
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            if re.match(r"^[\w-]+\s*:", line):
                break
            if not re.match(r"^\s*-\s+", line):
                raise ValueError("unsupported sources recovery syntax")
            block.append(line)
        try:
            data = {"sources": yaml.safe_load("\n".join(block)) or []}
        except yaml.YAMLError as exc:
            raise ValueError("malformed sources list") from exc
        recovered = True
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    paths = data.get("sources", [])
    if not isinstance(paths, list) or any(not isinstance(p, str) for p in paths):
        raise ValueError("sources must be a list of strings")
    if any(not p.startswith("raw/") for p in paths):
        raise ValueError("sources contains a path outside raw/")
    return paths, recovered


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directories", nargs="+", type=Path)
    args = parser.parse_args()
    paths = set()
    failed = False
    for directory in args.directories:
        if not directory.is_dir():
            print(f"ERROR: missing directory: {directory}", file=sys.stderr)
            failed = True
            continue
        for file in sorted(directory.rglob("*.md")):
            try:
                found, recovered = extract_sources(file.read_text())
                paths.update(found)
                if recovered:
                    print(f"WARNING: recovered sources from malformed YAML: {file}", file=sys.stderr)
            except (ValueError, OSError) as exc:
                print(f"ERROR: {file}: {exc}", file=sys.stderr)
                failed = True
    if failed:
        return 1
    print("\n".join(sorted(paths)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
