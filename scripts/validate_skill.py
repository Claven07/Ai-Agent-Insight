from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_FILE = ROOT / "SKILL.md"
DIST_DIR = ROOT / "dist"
PACKAGE_NAME = "ai-agent-insights-0.1.0.zip"

# Keep development notes and test fixtures out of the marketplace upload.
# The upload contains the actual skill, its licence, and its required references.
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
MAX_WEBSITE_ZIP_BYTES = 50 * 1024 * 1024
MAX_WEBSITE_FILES = 1000

SECRET_PATTERNS = (
    re.compile(r"\b(?:sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})\b"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
)

# Agensi documents these literal prompt-injection examples as scan signals.
PROMPT_INJECTION_PATTERNS = (
    re.compile(r"(?i)ignore\s+previous\s+instructions"),
    re.compile(r"(?i)do\s+not\s+tell\s+the\s+user"),
    re.compile(r"(?i)\bsecretly\b"),
)

DANGEROUS_COMMAND_PATTERNS = (
    re.compile(r"(?i)\bos\.system\s*\("),
    re.compile(r"(?i)\bshell\s*=\s*true\b"),
    re.compile(r"(?i)\bchmod\s+777\b"),
    re.compile(r"(?i)(?:curl|wget)\b[^\n|]*\|\s*(?:sh|bash)\b"),
)

DISALLOWED_EXTENSIONS = {
    ".exe", ".dll", ".jar", ".wasm", ".bin", ".so", ".dylib",
    ".app", ".dmg", ".msi", ".deb", ".rpm", ".class", ".war",
}

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
    if not parts[2].strip():
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

    # Agensi's current packaging guide requires name and description.
    # Other listing metadata is optional; validate its type without inventing
    # undocumented maximum counts or character limits.
    for field in ("summary", "version", "docs_url"):
        value = metadata.get(field)
        if value is not None and not isinstance(value, str):
            fail(f"Optional frontmatter field '{field}' must be a string.")

    for field in ("tags", "keywords", "use_cases"):
        values = metadata.get(field)
        if values is not None:
            if not isinstance(values, list) or any(
                not isinstance(item, str) or not item.strip() for item in values
            ):
                fail(f"Optional frontmatter field '{field}' must be a list of non-empty strings.")
            if len(set(values)) != len(values):
                fail(f"Optional frontmatter field '{field}' contains duplicates.")

    docs_url = metadata.get("docs_url")
    if docs_url is not None and not docs_url.startswith("https://"):
        fail("Frontmatter 'docs_url' must be an HTTPS URL.")

def validate_references(skill_text: str) -> set[Path]:
    referenced_strings = set(re.findall(r"references/[A-Za-z0-9_.-]+\.md", skill_text))
    if not referenced_strings:
        fail("SKILL.md does not reference any supporting methodology files.")

    referenced: set[Path] = set()
    for value in sorted(referenced_strings):
        relative = Path(value)
        if not (ROOT / relative).is_file():
            fail(f"SKILL.md references a missing file: {value}")
        referenced.add(relative)

    packaged_references = {path for path in PACKAGE_FILES if path.parts[:1] == ("references",)}
    if not referenced.issubset(packaged_references):
        fail("A referenced methodology file is not included in the marketplace package.")
    return referenced

def parse_timestamp(value: str) -> datetime:
    if not isinstance(value, str):
        fail("Concurrency fixture timestamp must be a string.")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        fail(f"Invalid concurrency fixture timestamp: {value} ({exc})")

def has_complete_interval(item: dict[str, Any]) -> bool:
    return bool(item.get("started_at") and item.get("ended_at"))

def intervals_overlap(first: dict[str, Any], second: dict[str, Any]) -> bool:
    if not has_complete_interval(first) or not has_complete_interval(second):
        return False
    first_start = parse_timestamp(first["started_at"])
    first_end = parse_timestamp(first["ended_at"])
    second_start = parse_timestamp(second["started_at"])
    second_end = parse_timestamp(second["ended_at"])
    return first_start < second_end and second_start < first_end

def validate_concurrency_fixture() -> dict[str, int]:
    path = ROOT / "examples/sample-session-concurrency.json"
    challenge = json.loads(path.read_text(encoding="utf-8"))
    tools = challenge["tool_calls"]
    requests = challenge["llm_requests"]

    tool_successes = sum(item.get("status") == "success" for item in tools)
    tool_failures = sum(item.get("status") != "success" for item in tools)
    llm_successes = sum(item.get("status") == "success" for item in requests)
    llm_failures = sum(item.get("status") != "success" for item in requests)

    if challenge["session"]["duration_ms"] != 12000:
        fail("Concurrency fixture session duration expectation failed.")
    if (len(tools), tool_successes, tool_failures) != (5, 2, 3):
        fail("Concurrency fixture tool record/outcome expectations failed.")
    if (len(requests), llm_successes, llm_failures) != (3, 1, 2):
        fail("Concurrency fixture LLM record/outcome expectations failed.")
    if sum(item["duration_ms"] for item in tools) != 11000:
        fail("Concurrency fixture cumulative tool duration expectation failed.")
    if sum(item["duration_ms"] for item in requests) != 7300:
        fail("Concurrency fixture cumulative LLM duration expectation failed.")
    if any("logical_operation_id" in item for item in tools):
        fail("Concurrency fixture must omit logical tool-operation IDs.")
    if any("logical_request_id" in item for item in requests):
        fail("Concurrency fixture must omit logical LLM-request IDs.")

    complete_tool_intervals = sum(has_complete_interval(item) for item in tools)
    complete_llm_intervals = sum(has_complete_interval(item) for item in requests)
    if (complete_tool_intervals, complete_llm_intervals) != (4, 1):
        fail("Concurrency fixture timestamp-completeness expectations failed.")

    by_call_id = {item["call_id"]: item for item in tools}
    by_attempt_id = {item["attempt_id"]: item for item in requests}
    if not intervals_overlap(by_call_id["tool-001"], by_call_id["tool-002"]):
        fail("Concurrency fixture search_docs overlap expectation failed.")
    if not intervals_overlap(by_attempt_id["llm-attempt-001"], by_call_id["tool-001"]):
        fail("Concurrency fixture LLM/tool overlap expectation failed for tool-001.")
    if not intervals_overlap(by_attempt_id["llm-attempt-001"], by_call_id["tool-002"]):
        fail("Concurrency fixture LLM/tool overlap expectation failed for tool-002.")
    if not intervals_overlap(by_call_id["tool-004"], by_call_id["tool-005"]):
        fail("Concurrency fixture run_tests overlap expectation failed.")

    return {
        "concurrency_tool_records": len(tools),
        "concurrency_tool_successes": tool_successes,
        "concurrency_tool_failures": tool_failures,
        "concurrency_llm_attempts": len(requests),
        "concurrency_llm_successes": llm_successes,
        "concurrency_llm_failures": llm_failures,
        "concurrency_tool_intervals_anchored": complete_tool_intervals,
        "concurrency_llm_intervals_anchored": complete_llm_intervals,
    }

def validate_fixtures() -> dict[str, int]:
    complete_path = ROOT / "examples/sample-session.json"
    retry_path = ROOT / "examples/sample-session-failure.json"
    complete = json.loads(complete_path.read_text(encoding="utf-8"))
    retry = json.loads(retry_path.read_text(encoding="utf-8"))

    if complete["session"]["duration_ms"] != 12000:
        fail("Complete-session fixture duration does not match its expected value.")
    if len(complete["steps"]) != 3 or len(complete["tool_calls"]) != 3:
        fail("Complete-session fixture count expectations failed.")
    if max(complete["tool_calls"], key=lambda item: item["duration_ms"])["name"] != "run_tests":
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
        path = ROOT / relative
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            fail(f"Marketplace package files must be readable text: {relative} ({exc})")

        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                fail(f"Potential hard-coded secret detected in package source: {relative}")
        for pattern in PROMPT_INJECTION_PATTERNS:
            if pattern.search(content):
                fail(f"Prompt-injection scan signal detected in package source: {relative}")
        for pattern in DANGEROUS_COMMAND_PATTERNS:
            if pattern.search(content):
                fail(f"Dangerous-command scan signal detected in package source: {relative}")

    return PACKAGE_FILES

def build_and_validate_zip(files: list[Path]) -> Path:
    DIST_DIR.mkdir(exist_ok=True)
    archive = DIST_DIR / PACKAGE_NAME
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for relative in files:
            zf.write(ROOT / relative, arcname=relative.as_posix())

    if archive.stat().st_size > MAX_WEBSITE_ZIP_BYTES:
        fail("ZIP exceeds Agensi's current 50 MB website-upload limit.")

    with zipfile.ZipFile(archive, "r") as zf:
        bad_entry = zf.testzip()
        if bad_entry:
            fail(f"ZIP CRC validation failed for {bad_entry}.")

        entries = zf.namelist()
        if len(entries) > MAX_WEBSITE_FILES:
            fail("ZIP exceeds Agensi's current website-upload file-count limit.")
        if entries.count("SKILL.md") != 1:
            fail("Package must contain exactly one root SKILL.md.")
        if any(name.startswith("/") or ".." in Path(name).parts for name in entries):
            fail("Package contains an unsafe archive path.")
        if any(Path(name).suffix.lower() in DISALLOWED_EXTENSIONS for name in entries):
            fail("Package contains a file type disallowed by Agensi.")
        if len(entries) != len(files):
            fail("Unexpected number of ZIP entries.")
        for name in entries:
            try:
                zf.read(name).decode("utf-8")
            except UnicodeDecodeError:
                fail(f"ZIP contains a non-text or invalid UTF-8 file: {name}")

    return archive

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate AI Agent Insights sources and optionally build the Agensi ZIP."
    )
    parser.add_argument(
        "--build-package",
        action="store_true",
        help="Build dist/ai-agent-insights-0.1.0.zip after validation.",
    )
    args = parser.parse_args()

    metadata, skill_text = parse_skill()
    validate_frontmatter(metadata)
    references = validate_references(skill_text)
    fixture_counts = validate_fixtures()
    concurrency_counts = validate_concurrency_fixture()
    package_files = validate_package_sources()

    print("PASS: SKILL.md YAML frontmatter (required name/description and optional metadata types)")
    print("PASS: all linked reference files exist and are included in the ZIP")
    print("PASS: synthetic JSON fixtures, retry accounting, and concurrency/partial-telemetry expectations")
    print("PASS: package sources are UTF-8 text and clear local secret/injection/command preflight")
    print("Skill:", metadata["name"])
    print("Referenced methodology files:", len(references))
    print("Fixture checks:", json.dumps(fixture_counts, sort_keys=True))
    print("Concurrency checks:", json.dumps(concurrency_counts, sort_keys=True))

    if args.build_package:
        archive = build_and_validate_zip(package_files)
        print("PASS: ZIP integrity, root SKILL.md, file types, paths, file count, and size")
        print("Package:", archive)
        print("Package bytes:", archive.stat().st_size)

    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        ValueError, KeyError, TypeError, OSError, json.JSONDecodeError, yaml.YAMLError
    ) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
