"""Validate the Korean lecture corpus and the local content index."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
INDEX = ROOT / "content-index.js"
LOCAL_LINK = re.compile(r"!?\[[^\]]*\]\((?!https?://|mailto:|#)([^)]+)\)")
INDEX_ENTRY = re.compile(r'"(templates/[^"\n]+\.md)"')


def resolve_link(source: Path, target: str) -> Path:
    clean = target.split("#", 1)[0].strip().replace("%20", " ")
    if clean.startswith("templates/"):
        return ROOT / clean
    if clean.startswith("/"):
        return ROOT / clean.lstrip("/")
    return source.parent / clean


def validate_markdown(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    outside_code: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            outside_code.append(line)
    h1 = [line for line in outside_code if line.startswith("# ")]
    if len(h1) != 1:
        errors.append(f"{path.relative_to(ROOT)}: H1은 1개여야 합니다(현재 {len(h1)}개).")
    if text.count("```") % 2:
        errors.append(f"{path.relative_to(ROOT)}: 코드 펜스가 닫히지 않았습니다.")
    if text.count("<details") != text.count("</details>"):
        errors.append(f"{path.relative_to(ROOT)}: details 태그 수가 맞지 않습니다.")
    if not path.name.startswith("00_") and not re.search(r"^## 참고문헌", text, flags=re.MULTILINE):
        errors.append(f"{path.relative_to(ROOT)}: 참고문헌 섹션이 없습니다.")
    for raw_target in LOCAL_LINK.findall(text):
        target = raw_target.strip("<>")
        if not resolve_link(path, target).exists():
            errors.append(f"{path.relative_to(ROOT)}: 로컬 링크 대상이 없습니다: {target}")
    return errors


def validate_index() -> list[str]:
    text = INDEX.read_text(encoding="utf-8")
    entries = INDEX_ENTRY.findall(text)
    errors: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        if entry in seen:
            errors.append(f"content-index.js: 중복 항목: {entry}")
        seen.add(entry)
        if not (ROOT / entry).exists():
            errors.append(f"content-index.js: 존재하지 않는 파일: {entry}")
    return errors


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="영문 강의도 검사")
    args = parser.parse_args()

    pattern = "lectures_*/*.md" if args.all else "lectures_korean/*.md"
    paths = sorted(TEMPLATES.glob(f"*/{pattern}"))
    errors = validate_index()
    for path in paths:
        errors.extend(validate_markdown(path))

    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors))
        return 1
    print(f"OK: {len(paths)}개 강의 파일과 content-index.js를 검증했습니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
