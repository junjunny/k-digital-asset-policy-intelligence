#!/usr/bin/env python3
"""Fetch source documents, extract text, and compare Evidence excerpts.

Remote content is untrusted data. This script never executes scripts, macros,
links, or instructions found in a source document.
"""

import argparse
import hashlib
import io
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from copy import deepcopy
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:  # handled as a manual-review result for PDF inputs
    PdfReader = None

USER_AGENT = "K-DAPI-evidence-verifier/2.0 (+https://github.com/junjunny/k-digital-asset-policy-intelligence)"
RESTRICTED_CODES = {401, 403, 407, 429, 451}
INSTRUCTION_PATTERNS = (
    "ignore previous instructions",
    "ignore all previous instructions",
    "system prompt",
    "you are chatgpt",
    "이전 지시를 무시",
    "앞선 지시를 무시",
)


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.suppressed = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in {"script", "style", "noscript", "svg"}:
            self.suppressed += 1
        elif tag.lower() in {"p", "br", "li", "div", "tr", "h1", "h2", "h3", "h4", "section", "article"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag.lower() in {"script", "style", "noscript", "svg"} and self.suppressed:
            self.suppressed -= 1
        elif tag.lower() in {"p", "li", "div", "tr", "section", "article"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.suppressed:
            self.parts.append(data)

    def text(self):
        return " ".join("".join(self.parts).split())


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def normalize_text(value):
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("\u00a0", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def detect_untrusted_instructions(text):
    lowered = text.lower()
    return [pattern for pattern in INSTRUCTION_PATTERNS if pattern in lowered]


def decode_text(data, content_type):
    charset = None
    match = re.search(r"charset=([\w.-]+)", content_type or "", re.I)
    if match:
        charset = match.group(1)
    for encoding in [charset, "utf-8", "cp949", "euc-kr", "latin-1"]:
        if not encoding:
            continue
        try:
            return data.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            pass
    return data.decode("utf-8", errors="replace")


def extract_text(data, content_type, source_name):
    lowered_type = (content_type or "").lower()
    lowered_name = source_name.lower()
    if "pdf" in lowered_type or lowered_name.endswith(".pdf"):
        if PdfReader is None:
            raise RuntimeError("PDF extraction requires pypdf; install requirements.txt")
        reader = PdfReader(io.BytesIO(data))
        pages = []
        for number, page in enumerate(reader.pages, start=1):
            pages.append(f"[PAGE {number}]\n{page.extract_text() or ''}")
        return "\n".join(pages), "PDF_TEXT"
    decoded = decode_text(data, content_type)
    if "html" in lowered_type or "<html" in decoded[:1000].lower():
        parser = TextExtractor()
        parser.feed(decoded)
        return parser.text(), "HTML_TEXT"
    return normalize_text(decoded), "PLAIN_TEXT"


def fetch_url(url, timeout, max_bytes):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/pdf,text/plain,*/*"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise ValueError(f"document exceeds max size of {max_bytes} bytes")
        return {
            "data": data,
            "http_status": getattr(response, "status", None),
            "content_type": response.headers.get("Content-Type"),
            "final_url": response.geturl(),
        }


def base_result(method="URL_ONLY"):
    return {
        "status": "MANUAL_REVIEW_REQUIRED",
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "method": method,
        "http_status": None,
        "content_type": None,
        "final_url": None,
        "document_sha256": None,
        "extracted_text_sha256": None,
        "content_length": None,
        "excerpt_match": None,
        "matched_excerpt": None,
        "warnings": [],
        "error": None,
    }


def verify_record(record, base_dir, timeout=20, max_bytes=25_000_000):
    result = base_result()
    evidence_id = record.get("evidence_id", "UNKNOWN")
    fetched = False
    manual_path = record.get("manual_source_path")
    try:
        if manual_path:
            path = (base_dir / manual_path).resolve()
            data = path.read_bytes()
            if len(data) > max_bytes:
                raise ValueError(f"document exceeds max size of {max_bytes} bytes")
            response = {"data": data, "http_status": None, "content_type": None, "final_url": path.as_uri()}
            result["warnings"].append("MANUAL_ATTACHMENT_AUTHENTICITY_NOT_VERIFIED")
        else:
            response = fetch_url(record["official_url"], timeout, max_bytes)
        fetched = True
        data = response["data"]
        result.update({
            "http_status": response["http_status"],
            "content_type": response["content_type"],
            "final_url": response["final_url"],
            "document_sha256": sha256(data),
            "content_length": len(data),
        })
        text, method = extract_text(data, response["content_type"], response["final_url"] or manual_path or "")
        normalized_text = normalize_text(text)
        normalized_excerpt = normalize_text(record.get("relevant_excerpt", ""))
        result["method"] = "MANUAL_ATTACHMENT" if manual_path else method
        result["extracted_text_sha256"] = sha256(normalized_text.encode("utf-8"))
        injection_hits = detect_untrusted_instructions(normalized_text)
        if injection_hits:
            result["warnings"].append("UNTRUSTED_INSTRUCTION_PATTERN: " + ", ".join(injection_hits))
        if not normalized_excerpt:
            result["status"] = "MANUAL_REVIEW_REQUIRED"
            result["error"] = "relevant_excerpt is empty"
        elif normalized_excerpt in normalized_text:
            result["status"] = "CONTENT_VERIFIED"
            result["excerpt_match"] = True
            result["matched_excerpt"] = record["relevant_excerpt"]
        else:
            result["status"] = "CONTENT_MISMATCH"
            result["excerpt_match"] = False
            result["error"] = "normalized relevant_excerpt was not found in extracted source text"
    except urllib.error.HTTPError as exc:
        result["http_status"] = exc.code
        result["final_url"] = record.get("official_url")
        result["status"] = "ACCESS_RESTRICTED" if exc.code in RESTRICTED_CODES else "MANUAL_REVIEW_REQUIRED"
        result["error"] = f"HTTP {exc.code}: {exc.reason}"
    except (urllib.error.URLError, TimeoutError) as exc:
        result["status"] = "MANUAL_REVIEW_REQUIRED"
        result["error"] = f"network unavailable or timed out: {exc}"
    except Exception as exc:
        result["status"] = "URL_REACHABLE" if fetched and not manual_path else "MANUAL_REVIEW_REQUIRED"
        result["error"] = str(exc)
    return {"evidence_id": evidence_id, **result}


def load_records(path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload, payload
    if isinstance(payload, dict) and isinstance(payload.get("evidence"), list):
        return payload["evidence"], payload
    raise ValueError("input must be an evidence list or report with an evidence list")


def main():
    parser = argparse.ArgumentParser(description="Verify K-DAPI source content and excerpts")
    parser.add_argument("path", type=Path)
    parser.add_argument("--output", type=Path, required=True, help="verification results JSON")
    parser.add_argument("--write-evidence", type=Path, help="write a v2 evidence/report copy with verification results")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--max-bytes", type=int, default=25_000_000)
    args = parser.parse_args()
    try:
        records, payload = load_records(args.path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    results = [verify_record(record, args.path.parent, args.timeout, args.max_bytes) for record in records]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.write_evidence:
        updated = deepcopy(payload)
        updated_records = updated if isinstance(updated, list) else updated["evidence"]
        by_id = {item["evidence_id"]: item for item in results}
        for record in updated_records:
            result = by_id[record["evidence_id"]]
            record["schema_version"] = "2.0"
            record["status_checked_at"] = result["checked_at"][:10]
            record["verification"] = {key: value for key, value in result.items() if key != "evidence_id"}
            if result["status"] == "CONTENT_VERIFIED":
                record["verification_status"] = "VERIFIED"
            elif result["status"] in {"URL_REACHABLE", "CONTENT_MISMATCH"}:
                record["verification_status"] = "PARTIALLY_VERIFIED"
            else:
                record["verification_status"] = "NEEDS_REVIEW"
        args.write_evidence.parent.mkdir(parents=True, exist_ok=True)
        args.write_evidence.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts = {}
    for result in results:
        counts[result["status"]] = counts.get(result["status"], 0) + 1
    print("Verification results: " + ", ".join(f"{key}={value}" for key, value in sorted(counts.items())))
    print(f"Saved: {args.output}")
    if args.write_evidence:
        print(f"Saved v2 evidence: {args.write_evidence}")
    return 1 if any(item["status"] == "CONTENT_MISMATCH" for item in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())

