#!/usr/bin/env python3
"""Repository validator for clau-ai-core (stdlib only).

Checks:
  - required files exist
  - governance docs: frontmatter fields, SemVer, allowed status, latest
    Revision History row and README "Versi Dokumen" table all agree
  - relative Markdown links resolve
  - JSON files parse
  - no obvious secrets are committed

Usage: python scripts/validate_core.py   (exit 0 = pass, 1 = failures)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "README.md", "ACKNOWLEDGMENT.md", "LICENSE",
    "AI-CONSTITUTION.md", "AI-BOUNDARY.md", "AGENTS.md", "WORKFLOW.md",
    "orchestrator/README.md", "orchestrator/router.md",
    "orchestrator/decision-tree.md", "orchestrator/priority-engine.md",
    "shared/database-schema.md", "shared/api-contracts.md",
    "shared/data-flow.md", "shared/integrations.md",
    "docs/getting-started.md", "docs/5-pillar-architecture.md",
]
GOVERNANCE_DOCS = ["AI-CONSTITUTION.md", "AI-BOUNDARY.md", "WORKFLOW.md", "AGENTS.md"]
GOVERNANCE_FIELDS = ["document_title", "document_owner", "version", "status"]
DOC_STATUSES = {"Draft", "For Review", "Approved", "Superseded", "Archived"}
EVIDENCE_LABELS = ["DATA FINAL", "ASSUMPTION", "CLIENT CONFIRMATION", "FIELD VERIFICATION", "RISK", "NEXT ACTION"]

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
REVISION_ROW_RE = re.compile(r"^\|\s*(\d+\.\d+\.\d+)\s*\|\s*[^|]+\|\s*([^|]+?)\s*\|", re.MULTILINE)
README_ROW_RE = re.compile(r"^\|\s*\[([^\]]+)\]\([^)]+\)\s*\|\s*(\d+\.\d+\.\d+)\s*\|\s*([^|]+?)\s*\|", re.MULTILINE)
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__"}
SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"), "GitHub token"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"), "API secret key"),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"), "Google API key"),
    (re.compile(r"\bEAA[A-Za-z0-9]{40,}\b"), "Meta access token"),
]

failures: list[str] = []


def fail(path: Path | str, msg: str) -> None:
    rel = path.relative_to(ROOT) if isinstance(path, Path) else path
    failures.append(f"{rel}: {msg}")


def files(pattern: str) -> list[Path]:
    return sorted(p for p in ROOT.rglob(pattern)
                  if p.is_file() and not any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts))


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    data = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"')
    return data


def check_required() -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            fail(rel, "required file is missing")


def check_governance() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    listed = {n: (v, s) for n, v, s in README_ROW_RE.findall(readme)}
    for rel in GOVERNANCE_DOCS:
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        meta = frontmatter(text)
        missing = [f for f in GOVERNANCE_FIELDS if not meta.get(f)]
        if missing:
            fail(path, f"frontmatter missing: {', '.join(missing)}")
            continue
        version, status = meta["version"], meta["status"]
        if not SEMVER_RE.match(version):
            fail(path, f"version '{version}' is not SemVer")
        if status not in DOC_STATUSES:
            fail(path, f"status '{status}' not allowed")
        if status == "Approved" and not meta.get("approval_reference"):
            fail(path, "Approved document requires approval_reference")
        parts = text.split("Revision History", 1)
        rows = REVISION_ROW_RE.findall(parts[1]) if len(parts) == 2 else []
        if not rows:
            fail(path, "missing Revision History rows")
        elif rows[-1] != (version, status):
            fail(path, f"latest Revision History row {rows[-1]} != frontmatter ({version}, {status})")
        if listed.get(rel) != (version, status):
            fail("README.md", f"Versi Dokumen row for {rel} is {listed.get(rel)}, expected ({version}, {status})")
    constitution = (ROOT / "AI-CONSTITUTION.md")
    if constitution.is_file():
        text = constitution.read_text(encoding="utf-8")
        missing = [label for label in EVIDENCE_LABELS if label not in text]
        if missing:
            fail(constitution, f"missing evidence labels: {', '.join(missing)}")


def check_links() -> None:
    for path in files("*.md"):
        text = INLINE_CODE_RE.sub("", FENCE_RE.sub("", path.read_text(encoding="utf-8")))
        for target in LINK_RE.findall(text):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                continue
            file_part = target.split("#", 1)[0]
            if file_part and not (path.parent / file_part).resolve().exists():
                fail(path, f"broken relative link: {target}")


def check_json() -> None:
    for path in files("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(path, f"invalid JSON: {exc}")


def check_secrets() -> None:
    me = Path(__file__).resolve()
    for path in files("*"):
        if path.resolve() == me or path.suffix not in {".md", ".json", ".yml", ".yaml", ".py", ".txt", ""}:
            continue
        if path.name.startswith(".env") and path.name != ".env.example":
            fail(path, ".env files must not be committed")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern, label in SECRET_PATTERNS:
            if pattern.search(text):
                fail(path, f"possible secret detected ({label}); value not printed")


def main() -> int:
    check_required()
    check_governance()
    check_links()
    check_json()
    check_secrets()
    if failures:
        print(f"FAIL — {len(failures)} issue(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("PASS — clau-ai-core validated, no issues found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
