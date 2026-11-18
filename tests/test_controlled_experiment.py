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

    def test_atomic_checkpoint_replaces_complete_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            MODULE.write_json_atomic(path, {"status": "RUNNING"})
            MODULE.write_json_atomic(path, {"status": "COMPLETED"})
            self.assertEqual("COMPLETED", json.loads(path.read_text())["status"])

    def test_summary_handles_na_and_small_samples(self):
        self.assertEqual("N/A", MODULE.summarize([])["mean"])
        self.assertEqual(0.0, MODULE.summarize([5])["stddev"])


if __name__ == "__main__":
    unittest.main()
