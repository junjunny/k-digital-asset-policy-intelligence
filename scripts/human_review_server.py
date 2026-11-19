#!/usr/bin/env python3
"""Local-only, condition-blind human review server for the Phase 9 answers."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import shutil
import threading
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
COHORT = ROOT / "evaluations" / "controlled-experiment-claude"
BLIND_DIR = COHORT / "scores" / "blind-inputs"
MAPPING_PATH = COHORT / "scores" / "blind-mapping.json"
MANIFEST_PATH = COHORT / "manifest.json"
PROMPTS_DIR = ROOT / "evaluations" / "controlled-experiment" / "prompts"
STATIC_DIR = ROOT / "human_review_ui"
DEFAULT_DATA_DIR = COHORT / "human-review"
SCORE_FIELDS = {
    "factual_currentness": 25,
    "source_claim_fit": 20,
    "depth_completeness": 15,
    "korean_relevance": 15,
    "risk_uncertainty": 10,
    "intent": 10,
    "usability": 5,
}
LEAK_PATTERNS = (
    re.compile(r"K-DARI", re.I),
    re.compile(r"K-DAPI", re.I),
    re.compile(r"k-digital-asset-policy-intelligence", re.I),
    re.compile(r"(?:실험군|condition)\s*[:=]?\s*[ABCD]\b", re.I),
    re.compile(r"(?:run[_ -]?id|skill installed|스킬 적용)", re.I),
)
URL_RE = re.compile(r"https?://[^\s)\]>]+")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def empty_scores() -> dict[str, dict[str, Any]]:
    return {key: {"state": "PENDING", "value": None, "comment": ""} for key in SCORE_FIELDS}


def empty_review(blind_id: str) -> dict[str, Any]:
    return {
        "blind_id": blind_id, "version": 0, "status": "DRAFT", "reviewer_id": "",
        "scores": empty_scores(), "claims": [], "strengths": "", "errors": "",
        "omissions": "", "improvements": "", "overall_comment": "",
        "created_at": None, "updated_at": None, "completed_at": None,
    }


def validate_review(review: dict[str, Any], blind_id: str) -> list[str]:
    errors = []
    if review.get("blind_id") != blind_id:
        errors.append("blind_id mismatch")
    if review.get("status") not in {"DRAFT", "COMPLETED", "NEEDS_VERIFICATION"}:
        errors.append("invalid status")
    scores = review.get("scores")
    if not isinstance(scores, dict) or set(scores) != set(SCORE_FIELDS):
        errors.append("score fields mismatch")
    else:
        for field, maximum in SCORE_FIELDS.items():
            item = scores[field]
            if item.get("state") not in {"PENDING", "SCORED", "UNCONFIRMED"}:
                errors.append(f"{field}: invalid state")
            value = item.get("value")
            if item.get("state") == "SCORED" and (not isinstance(value, int) or not 0 <= value <= maximum):
                errors.append(f"{field}: score outside 0..{maximum}")
            if item.get("state") != "SCORED" and value is not None:
                errors.append(f"{field}: non-scored value must be null")
    claims = review.get("claims")
    if not isinstance(claims, list):
        errors.append("claims must be a list")
    else:
        for index, claim in enumerate(claims):
            if claim.get("verdict") not in {"MATCH", "MISMATCH", "UNVERIFIABLE"}:
                errors.append(f"claim {index}: invalid verdict")
            url = claim.get("official_url", "")
            if url and urlparse(url).scheme not in {"http", "https"}:
                errors.append(f"claim {index}: URL must be http(s)")
    if review.get("status") == "COMPLETED" and any(item.get("state") == "PENDING" for item in review.get("scores", {}).values()):
        errors.append("completed review cannot contain pending score fields")
    return errors


def total_score(review: dict[str, Any]) -> int | None:
    scores = review.get("scores", {})
    if any(scores.get(field, {}).get("state") != "SCORED" for field in SCORE_FIELDS):
        return None
    return sum(scores[field]["value"] for field in SCORE_FIELDS)


class ReviewStore:
    def __init__(self, data_dir: Path, blind_ids: list[str], dataset_id: str):
        self.data_dir = data_dir
        self.path = data_dir / "reviews.json"
        self.history_path = data_dir / "revision-history.jsonl"
        self.backups = data_dir / "backups"
        self.blind_ids = set(blind_ids)
        self.dataset_id = dataset_id
        self.lock = threading.RLock()
        self.data = self._load()

    def _fresh(self) -> dict[str, Any]:
        return {"schema_version": 1, "dataset_id": self.dataset_id, "reviewer_id": "", "created_at": now(), "updated_at": now(), "reviews": {}}

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            data = self._fresh()
            atomic_json(self.path, data)
            return data
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if data.get("dataset_id") != self.dataset_id:
            raise ValueError("reviews.json belongs to a different blind dataset")
        return data

    def get(self, blind_id: str) -> dict[str, Any]:
        with self.lock:
            return json.loads(json.dumps(self.data["reviews"].get(blind_id, empty_review(blind_id))))

    def save(self, blind_id: str, incoming: dict[str, Any], expected_version: int) -> dict[str, Any]:
        if blind_id not in self.blind_ids:
            raise KeyError(blind_id)
        errors = validate_review(incoming, blind_id)
        if errors:
            raise ValueError("; ".join(errors))
        with self.lock:
            current = self.data["reviews"].get(blind_id, empty_review(blind_id))
            if current["version"] != expected_version:
                raise RuntimeError("VERSION_CONFLICT")
            saved = json.loads(json.dumps(incoming))
            saved["version"] = expected_version + 1
            saved["created_at"] = current.get("created_at") or now()
            saved["updated_at"] = now()
            saved["completed_at"] = now() if saved["status"] == "COMPLETED" else None
            self.data["reviews"][blind_id] = saved
            if saved.get("reviewer_id"):
                self.data["reviewer_id"] = saved["reviewer_id"]
            self.data["updated_at"] = now()
            self.data_dir.mkdir(parents=True, exist_ok=True)
            with self.history_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps({"saved_at": now(), "blind_id": blind_id, "version": saved["version"], "reviewer_id": saved.get("reviewer_id", ""), "review": saved}, ensure_ascii=False) + "\n")
            atomic_json(self.path, self.data)
            return json.loads(json.dumps(saved))

    def summary(self) -> dict[str, Any]:
        reviews = self.data["reviews"]
        counts = {key: 0 for key in ("DRAFT", "COMPLETED", "NEEDS_VERIFICATION")}
        for review in reviews.values():
            counts[review["status"]] += 1
        return {"total": len(self.blind_ids), "started": len(reviews), "unreviewed": len(self.blind_ids) - len(reviews), **{k.lower(): v for k, v in counts.items()}, "updated_at": self.data["updated_at"]}

    def export_payload(self) -> dict[str, Any]:
        with self.lock:
            return json.loads(json.dumps(self.data))

    def backup(self) -> Path:
        with self.lock:
            self.backups.mkdir(parents=True, exist_ok=True)
            path = self.backups / f"reviews-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
            shutil.copy2(self.path, path)
            return path

    def restore(self, payload: dict[str, Any]) -> None:
        if payload.get("dataset_id") != self.dataset_id or payload.get("schema_version") != 1:
            raise ValueError("backup dataset/schema mismatch")
        reviews = payload.get("reviews")
        if not isinstance(reviews, dict) or not set(reviews).issubset(self.blind_ids):
            raise ValueError("backup contains invalid blind IDs")
        for blind_id, review in reviews.items():
            errors = validate_review(review, blind_id)
            if errors:
                raise ValueError(f"{blind_id}: {'; '.join(errors)}")
        with self.lock:
            self.backup()
            payload["updated_at"] = now()
            self.data = payload
            atomic_json(self.path, self.data)


class ReviewDataset:
    def __init__(self, cohort: Path = COHORT):
        self.cohort = cohort
        self.blind_dir = cohort / "scores" / "blind-inputs"
        self.ids = [f"R{i:03d}" for i in range(1, 121)]
        missing = [blind_id for blind_id in self.ids if not (self.blind_dir / f"{blind_id}.md").is_file()]
        if missing:
            raise FileNotFoundError(f"missing blind inputs: {missing}")
        mapping = json.loads((cohort / "scores" / "blind-mapping.json").read_text(encoding="utf-8"))["mapping"]
        self.run_by_blind = {item["blind_id"]: item["run_id"] for item in mapping}
        manifest = json.loads((cohort / "manifest.json").read_text(encoding="utf-8"))
        self.slot_by_run = {slot["run_id"]: slot for slot in manifest["slots"]}
        self.prompts = {kind: json.loads((PROMPTS_DIR / f"{kind}.json").read_text(encoding="utf-8")) for kind in ("general", "detailed")}
        digest = hashlib.sha256()
        for blind_id in self.ids:
            digest.update(blind_id.encode())
            digest.update((self.blind_dir / f"{blind_id}.md").read_bytes())
        self.dataset_id = digest.hexdigest()

    def item(self, blind_id: str) -> dict[str, Any]:
        if blind_id not in self.ids:
            raise KeyError(blind_id)
        text = (self.blind_dir / f"{blind_id}.md").read_text(encoding="utf-8")
        slot = self.slot_by_run[self.run_by_blind[blind_id]]
        question = self.prompts[slot["prompt_kind"]][slot["topic"]]
        links = []
        for url in URL_RE.findall(text):
            clean = url.rstrip(".,;\"")
            if clean not in links:
                links.append(clean)
        return {
            "blind_id": blind_id, "question": question, "answer_markdown": text,
            "source_links": links, "verification_date": "2026-11-18",
            "blind_integrity": "POTENTIAL_CONDITION_LEAK" if any(pattern.search(text) for pattern in LEAK_PATTERNS) else "CLEAR",
        }

    def integrity_report(self) -> dict[str, str]:
        return {blind_id: self.item(blind_id)["blind_integrity"] for blind_id in self.ids}


def csv_bytes(data: dict[str, Any]) -> bytes:
    output = io.StringIO()
    fields = ["blind_id", "reviewer_id", "status", "version", *SCORE_FIELDS, "total_score", "claims", "match", "mismatch", "unverifiable", "strengths", "errors", "omissions", "improvements", "overall_comment", "updated_at"]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for blind_id in sorted(data["reviews"]):
        review = data["reviews"][blind_id]
        claims = review.get("claims", [])
        row = {"blind_id": blind_id, "reviewer_id": review.get("reviewer_id", ""), "status": review["status"], "version": review["version"], "total_score": total_score(review), "claims": len(claims), "match": sum(c["verdict"] == "MATCH" for c in claims), "mismatch": sum(c["verdict"] == "MISMATCH" for c in claims), "unverifiable": sum(c["verdict"] == "UNVERIFIABLE" for c in claims), "strengths": review.get("strengths", ""), "errors": review.get("errors", ""), "omissions": review.get("omissions", ""), "improvements": review.get("improvements", ""), "overall_comment": review.get("overall_comment", ""), "updated_at": review.get("updated_at", "")}
        for field in SCORE_FIELDS:
            item = review["scores"][field]
            row[field] = item["value"] if item["state"] == "SCORED" else item["state"]
        writer.writerow(row)
    return output.getvalue().encode("utf-8-sig")


class App:
    def __init__(self, dataset: ReviewDataset, store: ReviewStore):
        self.dataset, self.store = dataset, store

    def handler(self):
        app = self
        class Handler(BaseHTTPRequestHandler):
            server_version = "KDARIHumanReview/1.0"

            def log_message(self, fmt, *args):
                print(f"[{self.log_date_time_string()}] {fmt % args}")

            def json_response(self, value: Any, status=200):
                raw = json.dumps(value, ensure_ascii=False).encode("utf-8")
                self.send_response(status); self.send_header("Content-Type", "application/json; charset=utf-8"); self.send_header("Content-Length", str(len(raw))); self.send_header("Cache-Control", "no-store"); self.end_headers(); self.wfile.write(raw)

            def body_json(self):
                length = int(self.headers.get("Content-Length", "0"))
                if length > 5_000_000: raise ValueError("request too large")
                return json.loads(self.rfile.read(length).decode("utf-8"))

            def do_GET(self):
                path = self.path.split("?", 1)[0]
                if path == "/api/index":
                    reviews = app.store.data["reviews"]
                    items = [{"blind_id": blind_id, "status": reviews.get(blind_id, {}).get("status", "UNREVIEWED"), "integrity": app.dataset.item(blind_id)["blind_integrity"]} for blind_id in app.dataset.ids]
                    return self.json_response({"items": items, "progress": app.store.summary(), "score_fields": SCORE_FIELDS, "reviewer_id": app.store.data.get("reviewer_id", "")})
                match = re.fullmatch(r"/api/answers/(R\d{3})", path)
                if match:
                    blind_id = match.group(1)
                    try: item = app.dataset.item(blind_id)
                    except KeyError: return self.json_response({"error": "not found"}, 404)
                    item["review"] = app.store.get(blind_id)
                    return self.json_response(item)
                if path == "/api/export.json":
                    raw = json.dumps(app.store.export_payload(), ensure_ascii=False, indent=2).encode("utf-8")
                    self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Disposition", 'attachment; filename="human-reviews.json"'); self.send_header("Content-Length", str(len(raw))); self.end_headers(); return self.wfile.write(raw)
                if path == "/api/export.csv":
                    raw = csv_bytes(app.store.export_payload())
                    self.send_response(200); self.send_header("Content-Type", "text/csv; charset=utf-8"); self.send_header("Content-Disposition", 'attachment; filename="human-reviews.csv"'); self.send_header("Content-Length", str(len(raw))); self.end_headers(); return self.wfile.write(raw)
                if path == "/api/integrity":
                    report = app.dataset.integrity_report()
                    return self.json_response({"potential_leaks": [key for key, value in report.items() if value != "CLEAR"], "count": sum(value != "CLEAR" for value in report.values())})
                name = "index.html" if path == "/" else path.lstrip("/")
                target = (STATIC_DIR / name).resolve()
                if STATIC_DIR.resolve() not in target.parents or not target.is_file():
                    return self.send_error(404)
                content_type = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8"}.get(target.suffix, "application/octet-stream")
                raw = target.read_bytes(); self.send_response(200); self.send_header("Content-Type", content_type); self.send_header("Content-Length", str(len(raw))); self.send_header("Cache-Control", "no-store"); self.end_headers(); self.wfile.write(raw)

            def do_PUT(self):
                match = re.fullmatch(r"/api/reviews/(R\d{3})", self.path)
                if not match: return self.json_response({"error": "not found"}, 404)
                try:
                    payload = self.body_json(); saved = app.store.save(match.group(1), payload["review"], int(payload["expected_version"]))
                    return self.json_response({"review": saved, "progress": app.store.summary()})
                except RuntimeError:
                    return self.json_response({"error": "VERSION_CONFLICT", "current": app.store.get(match.group(1))}, 409)
                except (ValueError, KeyError, TypeError) as exc:
                    return self.json_response({"error": str(exc)}, 400)

            def do_POST(self):
                if self.path == "/api/backup":
                    return self.json_response({"backup": str(app.store.backup().relative_to(ROOT))})
                if self.path == "/api/restore":
                    try: app.store.restore(self.body_json()); return self.json_response({"ok": True, "progress": app.store.summary()})
                    except (ValueError, json.JSONDecodeError) as exc: return self.json_response({"error": str(exc)}, 400)
                return self.json_response({"error": "not found"}, 404)
        return Handler


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    args = parser.parse_args()
    if args.host not in {"127.0.0.1", "localhost", "::1"}:
        raise SystemExit("human review server may only bind to localhost")
    dataset = ReviewDataset()
    store = ReviewStore(args.data_dir.resolve(), dataset.ids, dataset.dataset_id)
    server = ThreadingHTTPServer((args.host, args.port), App(dataset, store).handler())
    print(f"K-DARI Human Review: http://{args.host}:{args.port}")
    print(f"Data: {store.path}")
    print(f"Blind integrity warnings: {[k for k,v in dataset.integrity_report().items() if v != 'CLEAR']}")
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()


if __name__ == "__main__":
    main()
