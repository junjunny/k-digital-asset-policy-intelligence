import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_report import validate_report  # noqa: E402
from validate_sources import validate_records  # noqa: E402


class ValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(
            (ROOT / "examples/tokenization-case-study/report.json").read_text(encoding="utf-8")
        )

    def test_example_report_is_valid(self):
        errors, _ = validate_report(self.report)
        self.assertEqual([], errors)

    def test_missing_evidence_field_fails(self):
        record = copy.deepcopy(self.report["evidence"][0])
        del record["official_url"]
        errors, _ = validate_records([record])
        self.assertTrue(any("official_url" in error for error in errors))

    def test_duplicate_evidence_id_fails(self):
        record = copy.deepcopy(self.report["evidence"][0])
        errors, _ = validate_records([record, record])
        self.assertTrue(any("duplicate" in error for error in errors))

    def test_future_law_cannot_be_in_force(self):
        record = copy.deepcopy(self.report["evidence"][3])
        record["legal_status"] = "IN_FORCE"
        errors, _ = validate_records([record])
        self.assertTrue(any("future effective_date" in error for error in errors))

    def test_verified_finding_requires_evidence(self):
        report = copy.deepcopy(self.report)
        report["findings"][0]["evidence_ids"] = []
        errors, _ = validate_report(report)
        self.assertTrue(any("requires evidence" in error for error in errors))

    def test_unknown_evidence_reference_fails(self):
        report = copy.deepcopy(self.report)
        report["findings"][0]["evidence_ids"] = ["EV-NOT-THERE"]
        errors, _ = validate_report(report)
        self.assertTrue(any("unknown evidence" in error for error in errors))

    def test_policy_cannot_support_current_law_claim(self):
        report = copy.deepcopy(self.report)
        finding = report["findings"][3]
        finding["statement"] = "현행법에 따라 기관투자자 사모사채 토큰화가 현재 시행 중이다."
        errors, _ = validate_report(report)
        self.assertTrue(any("current-law wording" in error for error in errors))

    def test_draft_cannot_support_final_rule_claim(self):
        report = copy.deepcopy(self.report)
        finding = report["findings"][5]
        finding["classification"] = "VERIFIED_FACT"
        finding["statement"] = "자기자본 40억원 요건은 확정 규정이다."
        errors, _ = validate_report(report)
        self.assertTrue(any("draft regulation" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

