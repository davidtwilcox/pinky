"""Validate workspace docs and source extraction without accessing the wiki."""
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

import yaml

from source_paths import extract_sources

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    errors = []
    for name in ("AGENTS.md", "CLAUDE.md", "wiki_scope.yaml.example", ".gitignore"):
        if not (root / name).is_file():
            errors.append(f"Missing required file: {name}")
    template = root / "wiki_scope.yaml.example"
    if template.exists():
        try:
            config = yaml.safe_load(template.read_text())
            if config['wiki']['access'] != 'read-only' or config['wiki']['root'] != '<absolute_path_to_wiki>':
                errors.append("Template must be generic and read-only")
        except (yaml.YAMLError, KeyError, TypeError) as exc:
            errors.append(f"Invalid template: {exc}")
    for name in ('wiki_scope.yaml', '.wiki_root', '.claude/settings.local.json'):
        result = subprocess.run(['git', 'check-ignore', '-q', name], cwd=root)
        if result.returncode:
            errors.append(f"Local file is not ignored: {name}")
    files = list(root.glob('*.md')) + list((root / 'docs').rglob('*.md')) + list((root / '.claude/commands').glob('*.md'))
    for file in sorted(files):
        text = re.sub(r'^> ?', '', file.read_text(), flags=re.M)
        for block in re.findall(r'```(?:bash|sh)\s*\n(.*?)```', text, re.S):
            result = subprocess.run(['bash', '-n'], input=block, text=True, capture_output=True)
            if result.returncode:
                errors.append(f"{file.relative_to(root)}: invalid shell example: {result.stderr.strip()}")
        prose = re.sub(r'```.*?```', '', text, flags=re.S)
        # Inline Markdown links only; wiki links refer to the external vault.
        for target in re.findall(r'\]\(([^\s)]+)\)', prose):
            url = urlsplit(target.strip('<>'))
            if url.scheme or url.netloc or not url.path:
                continue
            if not (file.parent / unquote(url.path)).exists():
                errors.append(f"{file.relative_to(root)}: broken local link: {target}")
    paths = [f'raw/document {i}.md' for i in range(12)]
    block = '---\nsources:\n' + ''.join(f'  - {p}\n' for p in paths) + 'related:\n  - "[[concept]]"\n---\nsources:\n  - raw/body.md\n'
    fixtures = [
        (block, (paths, False)),
        (block.replace('"[[concept]]"', '"unterminated'), (paths, True)),
        ('---\nsources: [raw/a.md, raw/b.md]\n---', (['raw/a.md', 'raw/b.md'], False)),
        ('---\ntitle: No sources\n---', ([], False)),
    ]
    for text, expected in fixtures:
        try:
            if extract_sources(text) != expected:
                errors.append('Source extraction fixture produced incorrect paths')
        except ValueError as exc:
            errors.append(f'Source extraction fixture failed: {exc}')
    for text in ('---\nsources: raw/a.md\n---', '---\nsources: [wiki/a.md]\n---', '---\nsources:\n  - raw/a.md', 'No frontmatter'):
        try:
            extract_sources(text)
            errors.append('Invalid source fixture was silently accepted')
        except ValueError:
            pass
    return errors


if __name__ == '__main__':
    failures = validate()
    for failure in failures:
        print(f'FAIL: {failure}', file=sys.stderr)
    if failures:
        sys.exit(1)
    print('PASS: setup files, config template, ignore rules, local Markdown links, shell examples, and source extraction fixtures')
