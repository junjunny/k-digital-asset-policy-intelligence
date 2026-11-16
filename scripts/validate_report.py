#!/usr/bin/env python3
"""Validate cross-record invariants in a K-DAPI report JSON."""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from validate_sources import validate_records

CLASSIFICATIONS = {"VERIFIED_FACT", "SUPPORTED_INFERENCE", "UNVERIFIED", "NEEDS_REVIEW"}
CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}


def valid_date(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def validate_report(report):
    errors, warnings = [], []
    required = {"report_id", "title", "analysis_date", "jurisdictions", "research_question", "evidence", "findings", "limitations"}
    missing = sorted(required - set(report))
    if missing:
        return [f"report: missing fields: {', '.join(missing)}"], warnings
    analysis_date = valid_date(report["analysis_date"])
    if not analysis_date:
        errors.append("report: analysis_date must be YYYY-MM-DD")
    if not isinstance(report["limitations"], list) or not report["limitations"]:
        errors.append("report: limitations must contain at least one item")
    source_errors, source_warnings = validate_records(report["evidence"])
    errors.extend(source_errors)
    warnings.extend(source_warnings)
    evidence = {item.get("evidence_id"): item for item in report.get("evidence", []) if isinstance(item, dict)}

    findings = report.get("findings")
    if not isinstance(findings, list) or not findings:
        errors.append("report: findings must contain at least one item")
        return errors, warnings
    seen = set()
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            errors.append(f"finding {index}: must be an object")
            continue
        finding_id = finding.get("finding_id", f"finding {index}")
        for field in ("statement", "classification", "evidence_ids", "confidence", "jurisdiction", "as_of_date"):
            if field not in finding:
                errors.append(f"{finding_id}: missing {field}")
        if finding_id in seen:
            errors.append(f"{finding_id}: duplicate finding_id")
        seen.add(finding_id)
        classification = finding.get("classification")
        if classification not in CLASSIFICATIONS:
            errors.append(f"{finding_id}: invalid classification")
        if finding.get("confidence") not in CONFIDENCE:
            errors.append(f"{finding_id}: invalid confidence")
        evidence_ids = finding.get("evidence_ids", [])
        if not isinstance(evidence_ids, list):
            errors.append(f"{finding_id}: evidence_ids must be a list")
            continue
        if classification in {"VERIFIED_FACT", "SUPPORTED_INFERENCE"} and not evidence_ids:
            errors.append(f"{finding_id}: {classification} requires evidence")
        unknown = sorted(set(evidence_ids) - set(evidence))
        if unknown:
            errors.append(f"{finding_id}: unknown evidence IDs: {', '.join(unknown)}")
        as_of = valid_date(finding.get("as_of_date"))
        if not as_of:
            errors.append(f"{finding_id}: as_of_date must be YYYY-MM-DD")
        elif analysis_date and as_of != analysis_date:
            warnings.append(f"{finding_id}: as_of_date differs from report analysis_date")

        statement = str(finding.get("statement", ""))
        linked = [evidence[eid] for eid in evidence_ids if eid in evidence]
        if any(term in statement for term in ("현재 시행", "현행법", "현재 효력")):
            if linked and all(item.get("legal_status") != "IN_FORCE" for item in linked):
                errors.append(f"{finding_id}: current-law wording is unsupported by IN_FORCE evidence")
        if any(item.get("legal_status") == "DRAFT_REGULATION" for item in linked):
            if classification == "VERIFIED_FACT" and any(term in statement for term in ("확정", "시행 중", "의무화")):
                errors.append(f"{finding_id}: draft regulation cannot support a final/active rule claim")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Validate a K-DAPI report JSON")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        report = json.loads(args.path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if not isinstance(report, dict):
        print("ERROR: report must be a JSON object", file=sys.stderr)
        return 2
    errors, warnings = validate_report(report)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"OK: report validated ({len(report['evidence'])} evidence, {len(report['findings'])} findings)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

