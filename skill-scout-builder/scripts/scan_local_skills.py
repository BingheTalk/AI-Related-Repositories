#!/usr/bin/env python3
"""Discover local Agent Skills and rank them with lightweight lexical matching."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path


DEFAULT_RELATIVE_ROOTS = (
    Path(".agents/skills"),
    Path(".claude/skills"),
    Path(".codex/skills"),
)
TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+._]*|[\u3400-\u9fff]+", re.IGNORECASE)


def parse_frontmatter(path: Path) -> tuple[str, str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return path.parent.name, ""
    if not text.startswith("---"):
        return path.parent.name, ""
    end = text.find("\n---", 3)
    if end == -1:
        return path.parent.name, ""
    block = text[3:end]
    values: dict[str, str] = {}
    for line in block.splitlines():
        match = re.match(r"^(name|description):\s*(.*)$", line.strip())
        if match:
            values[match.group(1)] = match.group(2).strip().strip("\"'")
    return values.get("name", path.parent.name), values.get("description", "")


def english_stem(token: str) -> str:
    if not token.isascii() or len(token) < 4:
        return token
    for suffix in ("ations", "ation", "itions", "ition", "ments", "ment", "ing", "ers", "ors", "ed", "er", "or", "es", "s"):
        if token.endswith(suffix) and len(token) - len(suffix) >= 3:
            token = token[: -len(suffix)]
            break
    if token.endswith("e") and len(token) > 4:
        token = token[:-1]
    return token


def tokenize(value: str) -> set[str]:
    tokens: set[str] = set()
    for raw in TOKEN_RE.findall(value.replace("-", " ")):
        token = raw.lower()
        tokens.add(token)
        if token.isascii():
            tokens.add(english_stem(token))
        elif len(token) > 1:
            tokens.update(token[index : index + 2] for index in range(len(token) - 1))
    return tokens


def score_candidate(name: str, description: str, query: str) -> int:
    if not query.strip():
        return 0
    query_tokens = tokenize(query)
    name_tokens = tokenize(name)
    description_tokens = tokenize(description)
    score = 5 * len(query_tokens & name_tokens)
    score += 2 * len(query_tokens & description_tokens)
    lowered = f"{name} {description}".lower()
    for phrase in (part.strip().lower() for part in query.split(",")):
        if phrase and phrase in lowered:
            score += 4
    return score


def default_roots() -> list[Path]:
    roots: list[Path] = []
    cwd = Path.cwd().resolve()
    for base in (cwd, *cwd.parents):
        roots.extend(base / relative for relative in DEFAULT_RELATIVE_ROOTS)
    home = Path.home()
    roots.extend(
        (
            home / ".agents/skills",
            home / ".claude/skills",
            home / ".codex/skills",
        )
    )
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        roots.append(Path(codex_home).expanduser() / "skills")
    claude_config = os.environ.get("CLAUDE_CONFIG_DIR")
    if claude_config:
        roots.append(Path(claude_config).expanduser() / "skills")
    extra_roots = os.environ.get("AGENT_SKILLS_DIRS", "")
    roots.extend(Path(value) for value in extra_roots.split(os.pathsep) if value)
    roots.append(Path("/etc/codex/skills"))
    return roots


def unique_existing_roots(values: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    result: list[Path] = []
    for value in values:
        try:
            resolved = value.expanduser().resolve()
        except OSError:
            continue
        if resolved in seen or not resolved.is_dir():
            continue
        seen.add(resolved)
        result.append(resolved)
    return result


def discover(roots: list[Path], query: str) -> list[dict[str, object]]:
    found: dict[Path, dict[str, object]] = {}
    for root in roots:
        for skill_file in root.rglob("SKILL.md"):
            if not skill_file.is_file():
                continue
            resolved = skill_file.resolve()
            if resolved in found:
                continue
            name, description = parse_frontmatter(resolved)
            found[resolved] = {
                "name": name,
                "description": description,
                "path": str(resolved.parent),
                "skill_file": str(resolved),
                "source_root": str(root),
                "score": score_candidate(name, description, query),
            }
    return sorted(
        found.values(),
        key=lambda item: (-int(item["score"]), str(item["name"]).lower(), str(item["path"])),
    )


def render_markdown(candidates: list[dict[str, object]]) -> str:
    lines = ["| Score | Skill | Description | Path |", "| ---: | --- | --- | --- |"]
    for item in candidates:
        description = str(item["description"]).replace("|", "\\|")
        lines.append(
            f"| {item['score']} | {item['name']} | {description} | `{item['path']}` |"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", action="append", default=[], help="Skill root to scan; repeatable")
    parser.add_argument("--query", default="", help="Comma-separated or free-text search terms")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--min-score", type=int, default=None, help="Minimum lexical score")
    args = parser.parse_args()

    requested = [Path(value) for value in args.root] if args.root else default_roots()
    roots = unique_existing_roots(requested)
    minimum = args.min_score if args.min_score is not None else (1 if args.query.strip() else 0)
    candidates = [item for item in discover(roots, args.query) if int(item["score"]) >= minimum]
    candidates = candidates[: max(args.limit, 0)]
    payload = {"roots": [str(root) for root in roots], "count": len(candidates), "candidates": candidates}
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(candidates))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
