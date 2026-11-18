import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class EvaluatorSchemaTests(unittest.TestCase):
    def test_schema_has_bounded_score_components(self):
        schema = json.loads((ROOT / "evaluations/controlled-experiment/scores/evaluator-schema.json").read_text())
        props = schema["properties"]["scores"]["items"]["properties"]
        expected = {
            "factual_currentness": 25,
            "source_claim_fit": 20,
            "depth_completeness": 15,
            "korean_relevance": 15,
            "risk_uncertainty": 10,
            "intent": 10,
            "usability": 5,
        }
        self.assertEqual(100, sum(expected.values()))
        for field, maximum in expected.items():
            self.assertEqual(maximum, props[field]["maximum"])

    def test_human_review_is_not_part_of_automatic_schema(self):
        text = (ROOT / "evaluations/controlled-experiment/scores/evaluator-schema.json").read_text()
        self.assertNotIn("human_score", text)


if __name__ == "__main__":
    unittest.main()
