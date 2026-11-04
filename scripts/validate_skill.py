from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_FILE = ROOT / "SKILL.md"
DIST_DIR = ROOT / "dist"
PACKAGE_NAME = "ai-agent-insights-0.1.0.zip"

# Ship only the actual skill, its licence, and referenced methodology files.
# Development docs and test fixtures remain in GitHub, not in the marketplace ZIP.
PACKAGE_FILES = [
    Path("SKILL.md"),
    Path("LICENSE"),
    Path("references/metrics-analysis.md"),
    Path("references/bottleneck-detection.md"),
    Path("references/llm-failure-analysis.md"),
    Path("references/report-standards.md"),
    Path("references/input-normalization.md"),
]

REQUIRED_FRONTMATTER = ("name", "description")
MAX_SUMMARY_CHARS = 300
MAX_TAGS = 10
MAX_KEYWORDS = 10
MAX_USE_CASES = 8

SECRET_PATTERNS = (
    re.compile(r"\b(?:sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})\b"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
)

def fail(message: str) -> None:
    raise ValueError(message)

def parse_skill() -> tuple[dict[str, Any], str]:
    if not SKILL_FILE.is_file():
        fail("Root SKILL.md is missing.")
    text = SKILL_FILE.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must begin with YAML frontmatter delimiter '---'.")
    parts = text.split("---", 2)
    if len(parts) != 3:
        fail("SKILL.md must contain opening and closing frontmatter delimiters.")
    metadata = yaml.safe_load(parts[1])
    if not isinstance(metadata, dict):
        fail("SKILL.md frontmatter must parse to a YAML mapping.")
    body = parts[2].strip()
    if not body:
        fail("SKILL.md body is empty.")
    return metadata, text

def require_string(metadata: dict[str, Any], field: str) -> str:
    value = metadata.get(field)
    if not isinstance(value, str) or not value.strip():
        fail(f"Frontmatter field '{field}' must be a non-empty string.")
    return value.strip()

def validate_frontmatter(metadata: dict[str, Any]) -> None:
    for field in REQUIRED_FRONTMATTER:
        require_string(metadata, field)

    name = require_string(metadata, "name")
    if len(name) > 60:
        fail("Skill name exceeds Agensi's 60-character listing limit.")

    summary = metadata.get("summary")
    if summary is not None:
        if not isinstance(summary, str):
            fail("Frontmatter 'summary' must be a string.")
        if len(summary) > MAX_SUMMARY_CHARS:
            fail(f"Summary exceeds {MAX_SUMMARY_CHARS} characters.")

    for field, limit in (
        ("tags", MAX_TAGS),
        ("keywords", MAX_KEYWORDS),
        ("use_cases", MAX_USE_CASES),
    ):
        values = metadata.get(field, [])
        if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
            fail(f"Frontmatter '{field}' must be a list of non-empty strings.")
        if len(values) > limit:
            fail(f"Frontmatter '{field}' exceeds the current Agensi limit of {limit}.")
        if len(set(values)) != len(values):
            fail(f"Frontmatter '{field}' contains duplicates.")

    version = metadata.get("version")
    if version is not None and not isinstance(version, (str, int, float)):
        fail("Frontmatter 'version' must be a string or number.")

    docs_url = metadata.get("docs_url")
    if docs_url is not None and (
        not isinstance(docs_url, str) or not docs_url.startswith("https://")
    ):
        fail("Frontmatter 'docs_url' must be an HTTPS URL.")

def validate_references(skill_text: str) -> None:
    referenced = set(re.findall(r"references/[A-Za-z0-9_.-]+\.md", skill_text))
    if not referenced:
        fail("SKILL.md does not reference any supporting methodology files.")
    for relative in sorted(referenced):
        if not (ROOT / relative).is_file():
            fail(f"SKILL.md references a missing file: {relative}")

def validate_fixtures() -> dict[str, int]:
    complete_path = ROOT / "examples/sample-session.json"
    retry_path = ROOT / "examples/sample-session-failure.json"
    complete = json.loads(complete_path.read_text(encoding="utf-8"))
    retry = json.loads(retry_path.read_text(encoding="utf-8"))

    if complete["session"]["duration_ms"] != 12000:
        fail("Complete-session fixture duration does not match its expected value.")
    if len(complete["steps"]) != 3:
        fail("Complete-session fixture should contain three steps.")
    if len(complete["tool_calls"]) != 3:
        fail("Complete-session fixture should contain three tool calls.")
    slowest_complete = max(complete["tool_calls"], key=lambda item: item["duration_ms"])
    if slowest_complete["name"] != "run_tests" or slowest_complete["duration_ms"] != 4100:
        fail("Complete-session fixture slowest-tool expectation failed.")

    tools = retry["tool_calls"]
    requests = retry["llm_requests"]
    tool_successes = sum(item["status"] == "success" for item in tools)
    tool_failures = sum(item["status"] == "error" for item in tools)
    logical_tool_operations = len({item["logical_operation_id"] for item in tools})
    logical_llm_requests = len({item["logical_request_id"] for item in requests})

    if (len(tools), tool_successes, tool_failures, logical_tool_operations) != (3, 2, 1, 2):
        fail("Retry fixture tool-attempt / logical-operation expectations failed.")
    if (len(requests), logical_llm_requests) != (2, 1):
        fail("Retry fixture LLM-attempt / logical-request expectations failed.")
    if max(tools, key=lambda item: item["duration_ms"])["duration_ms"] != 4500:
        fail("Retry fixture slowest-tool expectation failed.")

    return {
        "complete_session_steps": len(complete["steps"]),
        "complete_session_tool_calls": len(complete["tool_calls"]),
        "retry_tool_attempts": len(tools),
        "retry_tool_successes": tool_successes,
        "retry_tool_failures": tool_failures,
        "retry_logical_tool_operations": logical_tool_operations,
        "llm_attempts": len(requests),
        "logical_llm_requests": logical_llm_requests,
    }

def validate_package_sources() -> list[Path]:
    missing = [path.as_posix() for path in PACKAGE_FILES if not (ROOT / path).is_file()]
    if missing:
        fail("Missing package files: " + ", ".join(missing))

    for relative in PACKAGE_FILES:
        content = (ROOT / relative).read_text(encoding="utf-8")
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                fail(f"Potential hard-coded secret detected in package source: {relative}")

    return PACKAGE_FILES

def build_and_validate_zip(files: list[Path]) -> Path:
    DIST_DIR.mkdir(exist_ok=True)
    archive = DIST_DIR / PACKAGE_NAME
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for relative in files:
            zf.write(ROOT / relative, arcname=relative.as_posix())

    if archive.stat().st_size > 50 * 1024 * 1024:
        fail("ZIP exceeds Agensi's 50 MB website-upload limit.")

    with zipfile.ZipFile(archive, "r") as zf:
        bad_entry = zf.testzip()
        if bad_entry:
            fail(f"ZIP CRC validation failed for {bad_entry}.")
        entries = zf.namelist()
        if entries.count("SKILL.md") != 1:
            fail("Package must contain exactly one root SKILL.md.")
        if any(name.startswith("/") or ".." in Path(name).parts for name in entries):
            fail("Package contains an unsafe archive path.")
        if any(Path(name).suffix.lower() in {".exe", ".dll", ".jar", ".wasm", ".bin", ".so", ".dylib"} for name in entries):
            fail("Package contains a disallowed executable/binary file.")
        if len(entries) != len(files):
            fail("Unexpected number of ZIP entries.")

    return archive

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AI Agent Insights skill sources and optionally build the Agensi ZIP.")
    parser.add_argument("--build-package", action="store_true", help="Build dist/ai-agent-insights-0.1.0.zip after validation.")
    args = parser.parse_args()

    metadata, skill_text = parse_skill()
    validate_frontmatter(metadata)
    validate_references(skill_text)
    fixture_counts = validate_fixtures()
    package_files = validate_package_sources()

    print("PASS: SKILL.md YAML frontmatter and Agensi metadata constraints")
    print("PASS: referenced methodology files exist")
    print("PASS: synthetic JSON fixtures and retry-accounting expectations")
    print("PASS: package source inventory and hard-coded-secret preflight")
    print("Skill:", metadata["name"])
    print("Tags / keywords / use cases:",
          len(metadata.get("tags", [])), "/",
          len(metadata.get("keywords", [])), "/",
          len(metadata.get("use_cases", [])))
    print("Fixture checks:", json.dumps(fixture_counts, sort_keys=True))

    if args.build_package:
        archive = build_and_validate_zip(package_files)
        print("PASS: ZIP integrity, root SKILL.md, paths, file types and size")
        print("Package:", archive)
        print("Package bytes:", archive.stat().st_size)

    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
