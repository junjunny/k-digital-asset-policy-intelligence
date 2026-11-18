#!/usr/bin/env python3
"""Create, execute, blind, and aggregate the Phase 9 controlled experiment."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "evaluations" / "controlled-experiment"
MANIFEST = EXP / "manifest.json"
TOPICS = ("clarity_act", "ethereum", "usdc", "chainlink", "upbit", "token_securities")
CONDITIONS = {
    "A": (False, "general"),
    "B": (False, "detailed"),
    "C": (True, "general"),
    "D": (True, "detailed"),
}
SEED = 20261118
VALID_STATUSES = {"PLANNED", "RUNNING", "COMPLETED", "FAILED", "BLOCKED"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=path.name, suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_prompts() -> dict[str, dict[str, str]]:
    return {
        "general": read_json(EXP / "prompts" / "general.json"),
        "detailed": read_json(EXP / "prompts" / "detailed.json"),
    }


def build_manifest(seed: int = SEED) -> dict[str, Any]:
    prompts = load_prompts()
    slots = []
    for topic in TOPICS:
        for condition, (skill_installed, prompt_kind) in CONDITIONS.items():
            prompt = prompts[prompt_kind][topic]
            for repeat in range(1, 6):
                run_id = f"{topic}-{condition}-{repeat:02d}"
                slots.append({
                    "run_id": run_id,
                    "topic": topic,
                    "condition": condition,
                    "repeat": repeat,
                    "skill_installed": skill_installed,
                    "prompt_kind": prompt_kind,
                    "prompt_sha256": sha256_text(prompt),
                    "status": "PLANNED",
                    "attempts": [],
                    "selected_attempt": None,
                    "activation": "UNKNOWN" if skill_installed else "NOT_APPLICABLE",
                })
    random.Random(seed).shuffle(slots)
    return {
        "schema_version": 1,
        "seed": seed,
        "created_at": utc_now(),
        "design": "6 topics x 4 conditions x 5 repeats",
        "planned_slots": 120,
        "human_review_status": "HUMAN_REVIEW_PENDING",
        "slots": slots,
    }


def validate_manifest(data: dict[str, Any]) -> list[str]:
    errors = []
    slots = data.get("slots", [])
    if len(slots) != 120:
        errors.append(f"expected 120 slots, got {len(slots)}")
    ids = [slot.get("run_id") for slot in slots]
    if len(ids) != len(set(ids)):
        errors.append("run_id values are not unique")
    counts = {condition: 0 for condition in CONDITIONS}
    pair_hashes: dict[tuple[str, str], set[str]] = {}
    for slot in slots:
        condition = slot.get("condition")
        if condition not in CONDITIONS:
            errors.append(f"invalid condition: {condition}")
            continue
        counts[condition] += 1
        if slot.get("status") not in VALID_STATUSES:
            errors.append(f"invalid status for {slot.get('run_id')}")
        key = (slot.get("topic"), slot.get("prompt_kind"))
        pair_hashes.setdefault(key, set()).add(slot.get("prompt_sha256"))
    if any(value != 30 for value in counts.values()):
        errors.append(f"condition counts differ from 30: {counts}")
    if any(len(values) != 1 for values in pair_hashes.values()):
        errors.append("prompt hashes differ within a topic/prompt-kind pair")
    return errors


def parse_jsonl_events(text: str) -> tuple[str | None, dict[str, int] | None, bool]:
    """Extract final agent text, de-duplicated usage, and observed SKILL.md read."""
    final_text = None
    usage_events: dict[str, dict[str, int]] = {}
    activated = False
    for raw in text.splitlines():
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        serialized = json.dumps(event, ensure_ascii=False)
        if "SKILL.md" in serialized and "k-digital-asset-policy-intelligence" in serialized:
            activated = True
        item = event.get("item") if isinstance(event, dict) else None
        if isinstance(item, dict) and item.get("type") == "agent_message":
            final_text = item.get("text") or final_text
        usage = event.get("usage") if isinstance(event, dict) else None
        if isinstance(usage, dict):
            normalized = {k: int(v) for k, v in usage.items() if isinstance(v, int)}
            key = event.get("id") or hashlib.sha256(serialized.encode()).hexdigest()
            usage_events[str(key)] = normalized
    if not usage_events:
        return final_text, None, activated
    totals: dict[str, int] = {}
    for usage in usage_events.values():
        for key, value in usage.items():
            totals[key] = totals.get(key, 0) + value
    return final_text, totals, activated


def init_manifest(force: bool = False) -> None:
    if MANIFEST.exists() and not force:
        errors = validate_manifest(read_json(MANIFEST))
        if errors:
            raise SystemExit("invalid existing manifest: " + "; ".join(errors))
        print(f"kept existing manifest: {MANIFEST}")
        return
    manifest = build_manifest()
    write_json_atomic(MANIFEST, manifest)
    print(f"created {len(manifest['slots'])} slots: {MANIFEST}")


def record_environment() -> None:
    commands = {
        "codex": ["codex", "--version"],
        "python": [sys.executable, "--version"],
        "node": ["node", "--version"],
        "npm": ["npm", "--version"],
        "skills": ["npx", "--yes", "skills", "--version"],
        "git_head": ["git", "rev-parse", "HEAD"],
    }
    values: dict[str, Any] = {"captured_at": utc_now(), "cwd": str(ROOT)}
    for key, command in commands.items():
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
        values[key] = {"exit_code": result.returncode, "output": (result.stdout or result.stderr).strip()}
    write_json_atomic(EXP / "results" / "environment.json", values)
    print(EXP / "results" / "environment.json")


def selected_slots(manifest: dict[str, Any], args: argparse.Namespace) -> list[dict[str, Any]]:
    slots = manifest["slots"]
    if args.run_id:
        slots = [slot for slot in slots if slot["run_id"] == args.run_id]
    elif not args.all:
        raise SystemExit("choose --all or --run-id")
    if not args.retry:
        slots = [slot for slot in slots if slot["status"] in {"PLANNED", "RUNNING"}]
    return slots


def execute_slot(manifest: dict[str, Any], slot: dict[str, Any], args: argparse.Namespace) -> None:
    prompts = load_prompts()
    prompt = prompts[slot["prompt_kind"]][slot["topic"]]
    attempt_no = len(slot["attempts"]) + 1
    attempt_id = f"attempt-{attempt_no:02d}"
    run_dir = EXP / "runs" / slot["run_id"] / attempt_id
    run_dir.mkdir(parents=True, exist_ok=True)
    workdir = Path(args.skill_workdir if slot["skill_installed"] else args.control_workdir).resolve()
    isolated_home = Path(args.skill_home if slot["skill_installed"] else args.control_home).resolve()
    slot["status"] = "RUNNING"
    attempt = {"attempt_id": attempt_id, "started_at": utc_now(), "workdir_kind": "skill" if slot["skill_installed"] else "control"}
    slot["attempts"].append(attempt)
    write_json_atomic(MANIFEST, manifest)
    command = [
        "codex", "--search", "exec", "--json", "--ephemeral", "--ignore-user-config",
        "--model", args.model, "-c", f'model_reasoning_effort="{args.reasoning_effort}"',
        "--sandbox", "read-only", "--skip-git-repo-check", "-C", str(workdir), prompt,
    ]
    started = time.monotonic()
    environment = os.environ.copy()
    environment["HOME"] = str(isolated_home)
    environment["CODEX_HOME"] = str(isolated_home / ".codex")
    result = subprocess.run(command, text=True, capture_output=True, check=False, timeout=args.timeout, env=environment)
    duration = round(time.monotonic() - started, 3)
    (run_dir / "stdout.jsonl").write_text(result.stdout, encoding="utf-8")
    (run_dir / "stderr.txt").write_text(result.stderr, encoding="utf-8")
    final_text, usage, activated = parse_jsonl_events(result.stdout)
    if final_text:
        (run_dir / "answer.md").write_text(final_text.rstrip() + "\n", encoding="utf-8")
    attempt.update({
        "finished_at": utc_now(), "duration_seconds": duration, "exit_code": result.returncode,
        "usage": usage if usage is not None else "N/A", "answer_present": bool(final_text),
        "activation_observed": activated,
    })
    control_contaminated = activated and not slot["skill_installed"]
    attempt["control_contaminated"] = control_contaminated
    if result.returncode == 0 and final_text and not control_contaminated:
        attempt["analysis_valid"] = True
        slot["status"] = "COMPLETED"
        if slot["selected_attempt"] is None:
            slot["selected_attempt"] = attempt_id
        slot["activation"] = "CONFIRMED" if activated else ("UNKNOWN" if slot["skill_installed"] else "NOT_APPLICABLE")
    else:
        attempt["analysis_valid"] = False
        slot["status"] = "BLOCKED" if control_contaminated else "FAILED"
        failure = {"run_id": slot["run_id"], **attempt}
        failure_path = EXP / "results" / "failure-log.jsonl"
        failure_path.parent.mkdir(parents=True, exist_ok=True)
        with failure_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(failure, ensure_ascii=False) + "\n")
    write_json_atomic(MANIFEST, manifest)
    print(f"{slot['run_id']} {slot['status']} {duration}s activation={slot['activation']}", flush=True)


def run_experiment(args: argparse.Namespace) -> None:
    manifest = read_json(MANIFEST)
    errors = validate_manifest(manifest)
    if errors:
        raise SystemExit("; ".join(errors))
    for slot in selected_slots(manifest, args):
        try:
            execute_slot(manifest, slot, args)
        except subprocess.TimeoutExpired as exc:
            slot["status"] = "FAILED"
            slot["attempts"][-1].update({"finished_at": utc_now(), "failure": "TIMEOUT", "timeout_seconds": exc.timeout})
            write_json_atomic(MANIFEST, manifest)
            print(f"{slot['run_id']} FAILED timeout", flush=True)


def make_blind_copies() -> None:
    manifest = read_json(MANIFEST)
    completed = [slot for slot in manifest["slots"] if slot["status"] == "COMPLETED" and slot["selected_attempt"]]
    run_ids = [slot["run_id"] for slot in completed]
    shuffled = run_ids[:]
    random.Random(manifest["seed"] + 1).shuffle(shuffled)
    mapping = []
    blind_dir = EXP / "scores" / "blind-inputs"
    blind_dir.mkdir(parents=True, exist_ok=True)
    for index, run_id in enumerate(shuffled, 1):
        slot = next(item for item in completed if item["run_id"] == run_id)
        blind_id = f"R{index:03d}"
        answer = EXP / "runs" / run_id / slot["selected_attempt"] / "answer.md"
        shutil.copyfile(answer, blind_dir / f"{blind_id}.md")
        mapping.append({"blind_id": blind_id, "run_id": run_id})
    write_json_atomic(EXP / "scores" / "blind-mapping.json", {"seed": manifest["seed"] + 1, "mapping": mapping})
    print(f"created {len(mapping)} blind copies")


def invalidate_existing(reason: str) -> None:
    """Preserve attempts but exclude them from analysis and return slots to PLANNED."""
    manifest = read_json(MANIFEST)
    affected = 0
    for slot in manifest["slots"]:
        if slot["attempts"]:
            affected += 1
            for attempt in slot["attempts"]:
                attempt.setdefault("analysis_valid", False)
                attempt.setdefault("invalid_reason", reason)
            slot["status"] = "PLANNED"
            slot["selected_attempt"] = None
            slot["activation"] = "UNKNOWN" if slot["skill_installed"] else "NOT_APPLICABLE"
    manifest.setdefault("invalidations", []).append({"at": utc_now(), "reason": reason, "affected_slots": affected})
    write_json_atomic(MANIFEST, manifest)
    print(f"invalidated prior attempts in {affected} slots")


def summarize(values: list[float]) -> dict[str, Any]:
    if not values:
        return {key: "N/A" for key in ("n", "mean", "median", "stddev", "iqr", "min", "max")}
    ordered = sorted(values)
    quartiles = statistics.quantiles(ordered, n=4, method="inclusive") if len(values) > 1 else [ordered[0]] * 3
    return {
        "n": len(values), "mean": round(statistics.mean(values), 3), "median": round(statistics.median(values), 3),
        "stddev": round(statistics.stdev(values), 3) if len(values) > 1 else 0.0,
        "iqr": round(quartiles[2] - quartiles[0], 3), "min": min(values), "max": max(values),
    }


def aggregate() -> None:
    manifest = read_json(MANIFEST)
    score_path = EXP / "scores" / "automatic-scores.json"
    scores = read_json(score_path).get("scores", []) if score_path.exists() else []
    by_run = {item["run_id"]: item for item in scores if isinstance(item.get("total_score"), (int, float))}
    groups = {}
    topic_groups = {}
    slot_by_run = {slot["run_id"]: slot for slot in manifest["slots"]}
    for topic in TOPICS:
        topic_groups[topic] = {}
        for condition in CONDITIONS:
            subset = [slot for slot in manifest["slots"] if slot["topic"] == topic and slot["condition"] == condition]
            topic_values = [float(by_run[slot["run_id"]]["total_score"]) for slot in subset if slot["run_id"] in by_run]
            topic_groups[topic][condition] = {
                "planned": len(subset),
                "attempted": sum(bool(slot["attempts"]) for slot in subset),
                "succeeded": sum(slot["status"] == "COMPLETED" for slot in subset),
                "scored": len(topic_values),
                "activation_confirmed": sum(slot["activation"] == "CONFIRMED" for slot in subset),
                "score_summary": summarize(topic_values),
            }
    for condition in CONDITIONS:
        slots = [slot for slot in manifest["slots"] if slot["condition"] == condition]
        values = [float(by_run[slot["run_id"]]["total_score"]) for slot in slots if slot["run_id"] in by_run]
        selected_attempts = []
        for slot in slots:
            if not slot["selected_attempt"]:
                continue
            selected_attempts.extend(attempt for attempt in slot["attempts"] if attempt["attempt_id"] == slot["selected_attempt"])
        usage_exposed = [attempt["usage"] for attempt in selected_attempts if isinstance(attempt.get("usage"), dict)]
        total_tokens = sum(usage.get("input_tokens", 0) + usage.get("output_tokens", 0) for usage in usage_exposed)
        verified_claims = sum(by_run[slot["run_id"]].get("verified_core_claims", 0) for slot in slots if slot["run_id"] in by_run)
        groups[condition] = {
            "planned": len(slots),
            "attempted": sum(bool(slot["attempts"]) for slot in slots),
            "succeeded": sum(slot["status"] == "COMPLETED" for slot in slots),
            "scored": len(values),
            "activation_confirmed": sum(slot["activation"] == "CONFIRMED" for slot in slots),
            "failure_rate_of_attempted": round(sum(slot["status"] == "FAILED" for slot in slots) / max(1, sum(bool(slot["attempts"]) for slot in slots)), 4),
            "score_summary": summarize(values),
            "usage_exposed_runs": len(usage_exposed),
            "total_input_plus_output_tokens": total_tokens if usage_exposed else "N/A",
            "verified_core_claims": verified_claims if values else "N/A",
            "tokens_per_verified_core_claim": round(total_tokens / verified_claims, 3) if usage_exposed and verified_claims else "N/A",
        }
    means = {key: value["score_summary"]["mean"] for key, value in groups.items()}
    def contrast(left: str, right: str) -> float | str:
        if not isinstance(means[left], (int, float)) or not isinstance(means[right], (int, float)):
            return "N/A"
        return round(means[left] - means[right], 3)
    contrasts = {"C-B": contrast("C", "B"), "C-A": contrast("C", "A"), "D-B": contrast("D", "B"), "D-C": contrast("D", "C"), "B-A": contrast("B", "A")}
    contrasts["interaction_(D-C)-(B-A)"] = "N/A" if not all(isinstance(contrasts[key], (int, float)) for key in ("D-C", "B-A")) else round(contrasts["D-C"] - contrasts["B-A"], 3)
    relative = {}
    for label, difference in contrasts.items():
        if label.startswith("interaction") or not isinstance(difference, (int, float)):
            relative[label] = "N/A"
            continue
        right = label.split("-")[1]
        relative[label] = round(difference / means[right], 4) if isinstance(means[right], (int, float)) and means[right] != 0 else "N/A"
    output = {"generated_at": utc_now(), "human_review_status": "HUMAN_REVIEW_PENDING", "groups": groups, "topic_groups": topic_groups, "absolute_contrasts": contrasts, "relative_contrasts": relative}
    write_json_atomic(EXP / "results" / "aggregate.json", output)
    print(json.dumps(output, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    init_cmd = sub.add_parser("init")
    init_cmd.add_argument("--force", action="store_true")
    sub.add_parser("environment")
    run_cmd = sub.add_parser("run")
    run_cmd.add_argument("--all", action="store_true")
    run_cmd.add_argument("--run-id")
    run_cmd.add_argument("--retry", action="store_true")
    run_cmd.add_argument("--control-workdir", required=True)
    run_cmd.add_argument("--skill-workdir", required=True)
    run_cmd.add_argument("--control-home", required=True)
    run_cmd.add_argument("--skill-home", required=True)
    run_cmd.add_argument("--model", default="gpt-5.6-sol")
    run_cmd.add_argument("--reasoning-effort", default="medium")
    run_cmd.add_argument("--timeout", type=int, default=900)
    sub.add_parser("blind")
    sub.add_parser("aggregate")
    invalidate_cmd = sub.add_parser("invalidate-existing")
    invalidate_cmd.add_argument("--reason", required=True)
    args = parser.parse_args()
    if args.command == "init": init_manifest(args.force)
    elif args.command == "environment": record_environment()
    elif args.command == "run": run_experiment(args)
    elif args.command == "blind": make_blind_copies()
    elif args.command == "aggregate": aggregate()
    elif args.command == "invalidate-existing": invalidate_existing(args.reason)


if __name__ == "__main__":
    main()
