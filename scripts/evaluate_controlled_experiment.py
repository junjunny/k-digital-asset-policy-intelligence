#!/usr/bin/env python3
"""Prepare and run condition-blind, evidence-focused Phase 9 evaluations."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "evaluations" / "controlled-experiment"
TOPICS = ("clarity_act", "ethereum", "usdc", "chainlink", "upbit", "token_securities")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare() -> None:
    manifest = read_json(EXP / "manifest.json")
    mapping = read_json(EXP / "scores" / "blind-mapping.json")["mapping"]
    by_run = {item["run_id"]: item["blind_id"] for item in mapping}
    prompts = {kind: read_json(EXP / "prompts" / f"{kind}.json") for kind in ("general", "detailed")}
    slots = {slot["run_id"]: slot for slot in manifest["slots"]}
    out = EXP / "scores" / "evaluator-inputs"
    out.mkdir(parents=True, exist_ok=True)
    for topic in TOPICS:
        items = []
        for run_id, blind_id in sorted(by_run.items(), key=lambda pair: pair[1]):
            slot = slots[run_id]
            if slot["topic"] != topic:
                continue
            answer = (EXP / "scores" / "blind-inputs" / f"{blind_id}.md").read_text(encoding="utf-8")
            items.append({"blind_id": blind_id, "question": prompts[slot["prompt_kind"]][topic], "answer": answer})
        write_json(out / f"{topic}.json", {"topic": topic, "items": items})
    print("prepared condition-blind evaluator inputs")


def evaluator_prompt(topic: str) -> str:
    return f"""당신은 생성 에이전트와 분리된 증거 검증 평가자다. 현재 기준일은 2026-11-18이다.
현재 디렉터리의 {topic}.json에 있는 모든 답변을 조건을 추측하지 말고 평가하라.
rubric.md의 100점 기준을 적용하고, 각 답변의 중요한 사실을 웹에서 공식 1차 자료로 직접 대조하라.
법률안/현행법, 계획/실제 구현, 파일럿/상용화를 구분한다. 출처가 없거나 접근할 수 없으면 추측하지 않는다.
core claim 수와 VERIFIED/CONTRADICTED/INSUFFICIENT를 세고, 필수 항목 완성도와 표시 URL의 주장 적합성·1차 출처 비율을 기록하라.
비율 분모가 0이면 null을 사용한다. total_score는 7개 항목 합계와 정확히 같아야 한다.
각 답변에 사용한 핵심 공식 URL을 evidence_urls에 기록한다. 인간 승인이나 법률·투자 결론을 내리지 않는다.
출력은 지정된 JSON schema만 따른다."""


def run(topic: str, home: Path, model: str, reasoning_effort: str, timeout: int) -> None:
    input_dir = EXP / "scores" / "evaluator-inputs"
    output = EXP / "scores" / "evaluator-outputs" / f"{topic}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "codex", "--search", "exec", "--ephemeral", "--ignore-user-config", "--json",
        "--model", model, "-c", f'model_reasoning_effort="{reasoning_effort}"',
        "--sandbox", "read-only", "--skip-git-repo-check", "-C", str(input_dir),
        "--output-schema", str(EXP / "scores" / "evaluator-schema.json"),
        "--output-last-message", str(output), evaluator_prompt(topic),
    ]
    environment = os.environ.copy()
    environment["HOME"] = str(home)
    environment["CODEX_HOME"] = str(home / ".codex")
    raw = EXP / "scores" / "evaluator-outputs" / f"{topic}.jsonl"
    result = subprocess.run(command, text=True, capture_output=True, check=False, timeout=timeout, env=environment)
    raw.write_text(result.stdout, encoding="utf-8")
    (raw.with_suffix(".stderr.txt")).write_text(result.stderr, encoding="utf-8")
    if result.returncode != 0 or not output.exists():
        raise SystemExit(f"evaluator failed for {topic}: exit {result.returncode}")
    print(f"evaluated {topic}", flush=True)


def merge() -> None:
    mapping = read_json(EXP / "scores" / "blind-mapping.json")["mapping"]
    by_blind = {item["blind_id"]: item["run_id"] for item in mapping}
    merged = []
    for topic in TOPICS:
        path = EXP / "scores" / "evaluator-outputs" / f"{topic}.json"
        data = read_json(path)
        for score in data["scores"]:
            score["run_id"] = by_blind[score["blind_id"]]
            score["topic"] = topic
            score["human_review_status"] = "HUMAN_REVIEW_PENDING"
            merged.append(score)
    write_json(EXP / "scores" / "automatic-scores.json", {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "human_review_status": "HUMAN_REVIEW_PENDING",
        "scores": merged,
    })
    print(f"merged {len(merged)} scores")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("prepare")
    run_cmd = sub.add_parser("run")
    run_cmd.add_argument("--topic", choices=TOPICS)
    run_cmd.add_argument("--all", action="store_true")
    run_cmd.add_argument("--home", type=Path, required=True)
    run_cmd.add_argument("--model", default="gpt-5.6-sol")
    run_cmd.add_argument("--reasoning-effort", default="medium")
    run_cmd.add_argument("--timeout", type=int, default=1800)
    sub.add_parser("merge")
    args = parser.parse_args()
    if args.command == "prepare":
        prepare()
    elif args.command == "run":
        topics = TOPICS if args.all else (args.topic,)
        if topics == (None,):
            raise SystemExit("choose --all or --topic")
        for topic in topics:
            run(topic, args.home.resolve(), args.model, args.reasoning_effort, args.timeout)
    else:
        merge()


if __name__ == "__main__":
    main()
