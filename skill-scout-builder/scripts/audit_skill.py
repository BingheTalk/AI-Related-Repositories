#!/usr/bin/env python3
"""Flag security-sensitive patterns in a Skill directory for manual review."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TEXT_SUFFIXES = {
    "", ".md", ".txt", ".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".zsh",
    ".bash", ".fish", ".ps1", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg",
}
MAX_FILE_SIZE = 2_000_000

RULES = (
    ("critical", "policy-bypass", re.compile(r"ignore (?:all )?(?:previous|system|developer|user) instructions|bypass (?:approval|sandbox|policy)", re.I)),
    ("critical", "download-execute", re.compile(r"(?:curl|wget)[^\n|;]*(?:\||;|&&)\s*(?:sh|bash|zsh|python|node)\b", re.I)),
    ("high", "destructive-command", re.compile(r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f|git\s+reset\s+--hard|git\s+clean\s+-[a-zA-Z]*f", re.I)),
    ("high", "privilege-or-persistence", re.compile(r"\bsudo\b|/etc/(?:cron|launchd)|LaunchAgents|systemctl\s+enable|crontab\s+-", re.I)),
    ("high", "dynamic-execution", re.compile(r"\beval\s*\(|\bexec\s*\(|child_process\.exec|subprocess\.(?:Popen|run|call)[^\n]*shell\s*=\s*True", re.I)),
    ("high", "credential-access", re.compile(r"\.ssh/|\.aws/credentials|\.config/gcloud|keychain|security\s+find-generic-password|printenv|env\s*$", re.I)),
    ("medium", "encoded-payload", re.compile(r"base64\s+(?:-d|--decode)|frombase64string|atob\s*\(", re.I)),
    ("medium", "package-install", re.compile(r"\b(?:pip|pip3|npm|pnpm|yarn|brew|apt(?:-get)?)\s+install\b", re.I)),
    ("medium", "network-call", re.compile(r"https?://|\b(?:curl|wget)\b|requests\.(?:get|post|put|delete)|fetch\s*\(", re.I)),
    ("medium", "process-control", re.compile(r"\b(?:kill|pkill|killall)\b", re.I)),
    ("medium", "process-launch", re.compile(r"child_process\.spawn|subprocess\.(?:Popen|run|call)", re.I)),
    ("low", "broad-filesystem", re.compile(r"(?:Path\s*\(\s*['\"]/(?:Users|home|etc)|find\s+/(?:Users|home|etc)|chmod\s+-R)", re.I)),
)


def inspect_file(path: Path, root: Path) -> tuple[list[dict[str, object]], dict[str, object] | None]:
    relative = str(path.relative_to(root))
    try:
        size = path.stat().st_size
    except OSError as exc:
        return [], {"file": relative, "reason": f"stat failed: {exc}"}
    if size > MAX_FILE_SIZE:
        return [], {"file": relative, "reason": f"file exceeds {MAX_FILE_SIZE} bytes"}
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return [], {"file": relative, "reason": "binary or unsupported file type"}
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [], {"file": relative, "reason": f"read failed: {exc}"}

    findings: list[dict[str, object]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for severity, rule, pattern in RULES:
            if pattern.search(line):
                findings.append(
                    {
                        "severity": severity,
                        "rule": rule,
                        "file": relative,
                        "line": line_number,
                        "excerpt": line.strip()[:240],
                    }
                )
    return findings, None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", help="Directory containing the Skill to inspect")
    parser.add_argument("--format", choices=("json", "text"), default="text")
    args = parser.parse_args()

    root = Path(args.skill_dir).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    findings: list[dict[str, object]] = []
    skipped: list[dict[str, object]] = []
    files_reviewed = 0
    auditor_path = Path(__file__).resolve()
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            findings.append(
                {
                    "severity": "high",
                    "rule": "symlink",
                    "file": str(path.relative_to(root)),
                    "line": 0,
                    "excerpt": f"symlink target: {path.readlink()}",
                }
            )
            continue
        if not path.is_file():
            continue
        # The auditor's rule literals necessarily contain every pattern it detects.
        if path.resolve() == auditor_path:
            skipped.append({"file": str(path.relative_to(root)), "reason": "auditor rule definitions"})
            continue
        files_reviewed += 1
        file_findings, skip = inspect_file(path, root)
        findings.extend(file_findings)
        if skip:
            skipped.append(skip)

    payload = {
        "skill_dir": str(root),
        "files_reviewed": files_reviewed,
        "finding_count": len(findings),
        "findings": findings,
        "skipped": skipped,
        "note": "Static pattern matches require manual review; zero findings is not proof of safety.",
    }
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Reviewed {files_reviewed} files; found {len(findings)} signals; skipped {len(skipped)} files.")
        for item in findings:
            print(f"[{item['severity']}] {item['rule']} {item['file']}:{item['line']} {item['excerpt']}")
        for item in skipped:
            print(f"[info] skipped {item['file']}: {item['reason']}")
        print(payload["note"])
    return 1 if any(item["severity"] in {"critical", "high"} for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
