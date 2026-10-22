import copy
import unittest
from scripts.validate import ROOT, validate_config
from scripts.srs import next_due, review
import json

class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.c = json.loads((ROOT / "config/example.json").read_text())
    def test_public_example(self):
        validate_config(self.c, public=True)
    def test_bad_values(self):
        for field, value in [("default_minutes", 20), ("mode", "video"), ("timezone", "Invalid/Zone")]:
            c = copy.deepcopy(self.c)
            c["session"][field] = value
            with self.assertRaises(ValueError): validate_config(c)
    def test_missing_and_unknown_fields(self):
        for mutate in [lambda c: c.pop("target_language"), lambda c: c.update(secret="x")]:
            c = copy.deepcopy(self.c); mutate(c)
            with self.assertRaises(ValueError): validate_config(c)
    def test_private_only_notion_and_approval(self):
        self.c["notion"] = dict(enabled=False, destination=None, require_explicit_write_approval=True)
        validate_config(self.c)
        with self.assertRaises(ValueError): validate_config(self.c, public=True)
        self.c["notion"]["enabled"] = True
        with self.assertRaises(ValueError): validate_config(self.c)
        self.c["notion"]["destination"] = "fictional-destination"
        validate_config(self.c)
        self.c["notion"]["require_explicit_write_approval"] = False
        with self.assertRaises(ValueError): validate_config(self.c)
    def test_topics_and_context_required(self):
        for field, value in [("interests", []), ("context", {"life": [], "work": []})]:
            c = copy.deepcopy(self.c)
            c[field] = value
            with self.assertRaises(ValueError): validate_config(c)
        self.c["context"]["work"] = []
        self.c["level"]["self_reported"] = "unknown"
        validate_config(self.c)

    def test_same_language(self):
        self.c["target_language"] = self.c["native_language"]
        with self.assertRaises(ValueError): validate_config(self.c)

class SRSTests(unittest.TestCase):
    def setUp(self):
        self.e = dict(introduced_on="2024-02-28", passed_offsets=[], retry_on=None, reviews=[], status="learning")
    def test_calendar_offsets_and_cycle(self):
        for expected in ["2024-02-29", "2024-03-02", "2024-03-06", "2024-03-13"]:
            self.assertEqual(next_due(self.e), expected)
            self.e = review(self.e, expected, True)
        self.assertIsNone(next_due(self.e))
        self.assertEqual(self.e["status"], "cycle_complete")
    def test_overdue_does_not_skip_stages(self):
        e = review(self.e, "2024-03-20", True)
        self.assertEqual(e["passed_offsets"], [1])
        self.assertEqual(next_due(e), "2024-03-21")
        e = review(e, "2024-03-20", True)
        self.assertEqual(e["passed_offsets"], [1])
    def test_hints_and_missing_novel_use_do_not_pass(self):
        for kwargs in [dict(assisted=True), dict(novel_use=False)]:
            e = review(self.e, "2024-02-29", True, **kwargs)
            self.assertEqual(e["passed_offsets"], [])
            self.assertEqual(next_due(e), "2024-03-01")
    def test_early_practice(self):
        e = review(self.e, "2024-02-28", True)
        self.assertEqual(e["passed_offsets"], [])
        self.assertEqual(next_due(e), "2024-02-29")
    def test_failure_and_retry(self):
        e = review(self.e, "2024-02-29", False)
        e = review(e, "2024-03-01", True)
        self.assertEqual(e["passed_offsets"], [1])
        self.assertEqual(next_due(e), "2024-03-02")
    def test_reopen_and_immutability(self):
        original = copy.deepcopy(self.e)
        e = self.e
        for d in ["2024-02-29", "2024-03-02", "2024-03-06", "2024-03-13"]:
            e = review(e, d, True)
        e = review(e, "2024-04-01", False)
        self.assertEqual(next_due(e), "2024-04-02")
        self.assertEqual(e["passed_offsets"], [])
        self.assertEqual(len(e["reviews"]), 5)
        self.assertEqual(self.e, original)
    def test_reject_backdating(self):
        with self.assertRaises(ValueError): review(self.e, "2024-02-27", True)

if __name__ == "__main__": unittest.main()
