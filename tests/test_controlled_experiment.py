import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("controlled_experiment", ROOT / "scripts" / "controlled_experiment.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ControlledExperimentTests(unittest.TestCase):
    def test_manifest_has_120_balanced_slots_and_matching_prompt_hashes(self):
        manifest = MODULE.build_manifest()
        self.assertEqual([], MODULE.validate_manifest(manifest))
        self.assertEqual(120, len(manifest["slots"]))
        self.assertEqual({"HUMAN_REVIEW_PENDING"}, {manifest["human_review_status"]})

    def test_manifest_order_is_deterministic(self):
        first = [item["run_id"] for item in MODULE.build_manifest()["slots"]]
        second = [item["run_id"] for item in MODULE.build_manifest()["slots"]]
        self.assertEqual(first, second)

    def test_jsonl_parser_deduplicates_usage_and_detects_activation(self):
        usage = {"input_tokens": 10, "output_tokens": 4}
        lines = [
            json.dumps({"id": "u1", "usage": usage}),
            json.dumps({"id": "u1", "usage": usage}),
            json.dumps({"item": {"type": "command_execution", "command": "cat .agents/skills/k-digital-asset-policy-intelligence/SKILL.md"}}),
            json.dumps({"item": {"type": "agent_message", "text": "answer"}}),
        ]
        answer, totals, activated = MODULE.parse_jsonl_events("\n".join(lines))
        self.assertEqual("answer", answer)
        self.assertEqual(usage, totals)
        self.assertTrue(activated)

    def test_jsonl_parser_reports_na_when_usage_absent(self):
        answer, usage, activated = MODULE.parse_jsonl_events(json.dumps({"item": {"type": "agent_message", "text": "x"}}))
        self.assertEqual("x", answer)
        self.assertIsNone(usage)
        self.assertFalse(activated)

    def test_control_activation_is_detectable_as_contamination_signal(self):
        event = json.dumps({"item": {"type": "command_execution", "command": "cat ~/.agents/skills/k-digital-asset-policy-intelligence/SKILL.md"}})
        _, _, activated = MODULE.parse_jsonl_events(event)
        self.assertTrue(activated)

    def test_atomic_checkpoint_replaces_complete_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            MODULE.write_json_atomic(path, {"status": "RUNNING"})
            MODULE.write_json_atomic(path, {"status": "COMPLETED"})
            self.assertEqual("COMPLETED", json.loads(path.read_text())["status"])

    def test_summary_handles_na_and_small_samples(self):
        self.assertEqual("N/A", MODULE.summarize([])["mean"])
        self.assertEqual(0.0, MODULE.summarize([5])["stddev"])


class ClaudeRuntimeTests(unittest.TestCase):
    # Synthetic stream-json fixtures that exercise the parser only; they are not experiment data.
    def stream(self, *events):
        return "\n".join(json.dumps(e) for e in events)

    def test_claude_parser_uses_cumulative_result_usage_and_ignores_duplicate_messages(self):
        usage = {"input_tokens": 5, "output_tokens": 7, "cache_read_input_tokens": 100}
        text = self.stream(
            {"type": "system", "subtype": "init", "model": "m", "skills": ["x"]},
            {"type": "assistant", "message": {"id": "a", "usage": usage, "content": [{"type": "text", "text": "t"}]}},
            {"type": "assistant", "message": {"id": "a", "usage": usage, "content": [{"type": "tool_use", "name": "WebSearch", "input": {}}]}},
            {"type": "result", "result": "answer", "is_error": False, "usage": {"input_tokens": 9, "output_tokens": 7}, "total_cost_usd": 0},
        )
        parsed = MODULE.parse_claude_stream(text)
        self.assertEqual("answer", parsed["final_text"])
        self.assertEqual({"input_tokens": 9, "output_tokens": 7}, parsed["usage"])
        self.assertEqual(["WebSearch"], parsed["tool_calls"])
        self.assertFalse(parsed["activated"])

    def test_claude_parser_fallback_dedupes_by_message_id_and_na_when_absent(self):
        usage = {"input_tokens": 5, "output_tokens": 7}
        msg = {"type": "assistant", "message": {"id": "a", "usage": usage, "content": []}}
        self.assertEqual(usage, MODULE.parse_claude_stream(self.stream(msg, msg))["usage"])
        self.assertEqual("N/A", MODULE.parse_claude_stream("")["usage"])

    def test_claude_activation_requires_skill_tool_or_skill_md_read_not_similar_answer(self):
        skill = {"type": "assistant", "message": {"id": "s", "content": [{"type": "tool_use", "name": "Skill", "input": {"skill": MODULE.SKILL_NAME}}]}}
        read = {"type": "assistant", "message": {"id": "r", "content": [{"type": "tool_use", "name": "Read", "input": {"file_path": f"/x/.claude/skills/{MODULE.SKILL_NAME}/SKILL.md"}}]}}
        chat = {"type": "assistant", "message": {"id": "c", "content": [{"type": "text", "text": f"{MODULE.SKILL_NAME} SKILL.md"}]}}
        self.assertTrue(MODULE.parse_claude_stream(self.stream(skill))["activated"])
        self.assertTrue(MODULE.parse_claude_stream(self.stream(read))["activated"])
        self.assertFalse(MODULE.parse_claude_stream(self.stream(chat))["activated"])

    def test_failure_classifier_separates_auth_limit_and_unknown(self):
        self.assertEqual("AUTH_REQUIRED", MODULE.classify_claude_failure({"result": "Not logged in · Please run /login"}, ""))
        self.assertEqual("AUTH_REQUIRED", MODULE.classify_claude_failure({"result": "OAuth session expired"}, ""))
        self.assertEqual("USAGE_LIMIT", MODULE.classify_claude_failure({"result": "Claude usage limit reached"}, ""))
        self.assertIsNone(MODULE.classify_claude_failure({"result": "boom"}, ""))

    def test_blocked_auth_or_limit_slots_resume_but_contaminated_do_not(self):
        manifest = MODULE.build_manifest()
        a, b, c = manifest["slots"][:3]
        a.update(status="BLOCKED", attempts=[{"blocked_reason": "AUTH_REQUIRED"}])
        b.update(status="BLOCKED", attempts=[{"control_contaminated": True}])
        c.update(status="COMPLETED", attempts=[{}])
        args = type("A", (), {"run_id": None, "all": True, "retry": False})()
        ids = {slot["run_id"] for slot in MODULE.selected_slots(manifest, args)}
        self.assertIn(a["run_id"], ids)
        self.assertNotIn(b["run_id"], ids)
        self.assertNotIn(c["run_id"], ids)

    def test_claude_cohort_dir_is_separate_from_codex_cohort(self):
        self.assertEqual("controlled-experiment", MODULE.PROMPT_DIR.parent.name)


if __name__ == "__main__":
    unittest.main()
