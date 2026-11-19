#!/usr/bin/env python3
"""Apply the blind mapping only after an explicit human confirmation."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from human_review_server import COHORT, DEFAULT_DATA_DIR, SCORE_FIELDS, total_score


def stats(values):
    return {"n": len(values), "mean": round(statistics.mean(values), 3), "median": round(statistics.median(values), 3), "stddev": round(statistics.stdev(values), 3) if len(values) > 1 else 0.0} if values else {"n": 0, "mean": "N/A", "median": "N/A", "stddev": "N/A"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviews", type=Path, default=DEFAULT_DATA_DIR / "reviews.json")
    parser.add_argument("--output", type=Path, default=DEFAULT_DATA_DIR / "finalized-analysis.json")
    parser.add_argument("--confirm", required=True, help="must equal APPLY_BLIND_MAPPING")
    parser.add_argument("--allow-incomplete", action="store_true")
    args = parser.parse_args()
    if args.confirm != "APPLY_BLIND_MAPPING":
        raise SystemExit("refusing to reveal groups without --confirm APPLY_BLIND_MAPPING")
    data = json.loads(args.reviews.read_text(encoding="utf-8"))
    mapping = {item["blind_id"]: item["run_id"] for item in json.loads((COHORT / "scores" / "blind-mapping.json").read_text(encoding="utf-8"))["mapping"]}
    manifest = json.loads((COHORT / "manifest.json").read_text(encoding="utf-8"))
    slots = {slot["run_id"]: slot for slot in manifest["slots"]}
    completed = {key: value for key, value in data["reviews"].items() if value["status"] == "COMPLETED"}
    if len(completed) != 120 and not args.allow_incomplete:
        raise SystemExit(f"refusing incomplete finalization: {len(completed)}/120 completed")
    rows = []
    for blind_id, review in completed.items():
        slot = slots[mapping[blind_id]]
        rows.append({"blind_id": blind_id, "run_id": mapping[blind_id], "condition": slot["condition"], "topic": slot["topic"], "prompt_kind": slot["prompt_kind"], "total_score": total_score(review), "scores": review["scores"], "claims": review["claims"], "errors": review.get("errors", ""), "overall_comment": review.get("overall_comment", "")})
    groups = {}
    for condition in "ABCD":
        subset = [row for row in rows if row["condition"] == condition]
        totals = [row["total_score"] for row in subset if row["total_score"] is not None]
        components = {field: stats([row["scores"][field]["value"] for row in subset if row["scores"][field]["state"] == "SCORED"]) for field in SCORE_FIELDS}
        claims = [claim for row in subset for claim in row["claims"]]
        verdicts = Counter(claim["verdict"] for claim in claims)
        groups[condition] = {"total": stats(totals), "components": components, "claims": {"n": len(claims), "match_rate": round(verdicts["MATCH"] / len(claims), 4) if claims else "N/A", "mismatch_rate": round(verdicts["MISMATCH"] / len(claims), 4) if claims else "N/A", "unverifiable_rate": round(verdicts["UNVERIFIABLE"] / len(claims), 4) if claims else "N/A"}}
    topics = {topic: stats([row["total_score"] for row in rows if row["topic"] == topic and row["total_score"] is not None]) for topic in sorted({row["topic"] for row in rows})}
    means = {condition: groups[condition]["total"]["mean"] for condition in "ABCD"}
    def diff(left, right):
        return round(means[left] - means[right], 3) if isinstance(means[left], (int, float)) and isinstance(means[right], (int, float)) else "N/A"
    output = {"finalized_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "source_status": "HUMAN_REVIEW_COMPLETED" if len(completed) == 120 else "INCOMPLETE_ANALYSIS", "completed": len(completed), "groups": groups, "comparisons": {"C-A_general_skill_effect": diff("C", "A"), "C-B_skill_general_vs_detailed_no_skill": diff("C", "B"), "D-B_detailed_skill_effect": diff("D", "B"), "D-C_prompt_detail_with_skill": diff("D", "C"), "B-A_prompt_detail_without_skill": diff("B", "A")}, "topics": topics, "failure_cases": [{"blind_id": row["blind_id"], "run_id": row["run_id"], "condition": row["condition"], "topic": row["topic"], "total_score": row["total_score"], "errors": row["errors"], "overall_comment": row["overall_comment"]} for row in sorted(rows, key=lambda item: item["total_score"] if item["total_score"] is not None else 101)[:20]], "rows": rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
