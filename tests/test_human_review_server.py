import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("human_review_server", ROOT / "scripts" / "human_review_server.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class HumanReviewServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = MODULE.ReviewDataset()
        cls.original_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in cls.dataset.blind_dir.glob("R*.md")}

    @classmethod
    def tearDownClass(cls):
        after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in cls.dataset.blind_dir.glob("R*.md")}
        assert cls.original_hashes == after, "blind inputs changed during human-review tests"

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = MODULE.ReviewStore(Path(self.temp.name), self.dataset.ids, self.dataset.dataset_id)

    def tearDown(self):
        self.temp.cleanup()

    def test_all_120_blind_answers_load_without_condition_metadata(self):
        self.assertEqual(120, len(self.dataset.ids))
        for blind_id in self.dataset.ids:
            payload = self.dataset.item(blind_id)
            self.assertEqual(blind_id, payload["blind_id"])
            self.assertTrue(payload["question"])
            self.assertTrue(payload["answer_markdown"])
            self.assertEqual(
                {"blind_id", "question", "answer_markdown", "source_links", "verification_date", "blind_integrity"},
                set(payload),
            )
            for forbidden in ("run_id", "condition", "token_usage", "automatic_score", "blind_mapping"):
                self.assertNotIn(forbidden, payload)

    def test_integrity_scan_flags_known_answer_leak(self):
        self.assertEqual("POTENTIAL_CONDITION_LEAK", self.dataset.item("R019")["blind_integrity"])

    def test_empty_scores_are_pending_not_zero(self):
        review = MODULE.empty_review("R001")
        self.assertTrue(all(item["state"] == "PENDING" and item["value"] is None for item in review["scores"].values()))
        self.assertIsNone(MODULE.total_score(review))

    def test_save_reload_history_and_conflict_detection(self):
        review = MODULE.empty_review("R001")
        review["strengths"] = "test-only"
        saved = self.store.save("R001", review, 0)
        self.assertEqual(1, saved["version"])
        reloaded = MODULE.ReviewStore(Path(self.temp.name), self.dataset.ids, self.dataset.dataset_id)
        self.assertEqual("test-only", reloaded.get("R001")["strengths"])
        self.assertTrue(reloaded.history_path.read_text())
        with self.assertRaisesRegex(RuntimeError, "VERSION_CONFLICT"):
            self.store.save("R001", review, 0)

    def test_completed_review_allows_unconfirmed_without_zero_or_total(self):
        review = MODULE.empty_review("R002")
        review["status"] = "COMPLETED"
        for item in review["scores"].values():
            item["state"] = "UNCONFIRMED"
        saved = self.store.save("R002", review, 0)
        self.assertIsNone(MODULE.total_score(saved))
        csv_text = MODULE.csv_bytes(self.store.export_payload()).decode("utf-8-sig")
        self.assertIn("UNCONFIRMED", csv_text)

    def test_backup_and_restore(self):
        review = MODULE.empty_review("R003")
        first = self.store.save("R003", review, 0)
        backup = self.store.backup()
        payload = json.loads(backup.read_text())
        payload["reviews"]["R003"]["overall_comment"] = "restored"
        self.store.restore(payload)
        self.assertEqual("restored", self.store.get("R003")["overall_comment"])
        self.assertEqual(first["version"], self.store.get("R003")["version"])

    def test_review_client_does_not_reference_mapping(self):
        for name in ("index.html", "app.js"):
            text = (ROOT / "human_review_ui" / name).read_text()
            self.assertNotIn("blind-mapping", text)
            self.assertNotIn("condition", text)


if __name__ == "__main__":
    unittest.main()
