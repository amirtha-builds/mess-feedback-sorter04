"""Offline unit tests (no API key needed).  Run:  python -m unittest test_units -v"""
import unittest

from mess_sorter import (MANUAL_REVIEW, MockClient, apply_safety_net, classify, count_by_category,
                         find_actual_serving_time, find_health_terms, find_recurring_issues,
                         is_valid, meal_time_check, parse_reply, percent_negative)

GOOD = {"category": "hygiene", "sentiment": "negative", "urgent": True, "summary": "Insect found in sambar"}


class CountingClient:
    def __init__(self, replies):
        self.replies, self.calls = list(replies), 0
    def generate(self, system_prompt, user_message):
        self.calls += 1
        return self.replies.pop(0)


class ValidatorTests(unittest.TestCase):
    def test_valid_reply(self):
        self.assertTrue(is_valid(GOOD))
    def test_wrong_field_name(self):
        bad = dict(GOOD); bad["sentimnt"] = bad.pop("sentiment")
        self.assertFalse(is_valid(bad))
    def test_extra_field(self):
        self.assertFalse(is_valid({**GOOD, "confidence": 0.9}))
    def test_bad_category(self):
        self.assertFalse(is_valid({**GOOD, "category": "food"}))
    def test_urgent_must_be_bool(self):
        self.assertFalse(is_valid({**GOOD, "urgent": "true"}))
    def test_summary_over_12_words(self):
        self.assertFalse(is_valid({**GOOD, "summary": "one two three four five six seven eight nine ten eleven twelve thirteen"}))
    def test_parse_fenced_json(self):
        self.assertEqual(parse_reply('```json\n{"a": 1}\n```'), {"a": 1})
    def test_parse_plain_text_is_none(self):
        self.assertIsNone(parse_reply("Category: timing."))
    def test_parse_none(self):
        self.assertIsNone(parse_reply(None))


class ClassifyTests(unittest.TestCase):
    def test_empty_comment_never_calls_llm(self):
        client = CountingClient([])
        label, status, attempts = classify(client, "p", "   ")
        self.assertEqual((label["category"], status, attempts, client.calls), (MANUAL_REVIEW, "empty", 0, 0))
    def test_retry_once_then_ok(self):
        import json
        client = CountingClient(["not json", json.dumps(GOOD)])
        label, status, attempts = classify(client, "p", "Found an insect")
        self.assertEqual((status, attempts, client.calls), ("retried_ok", 2, 2))
    def test_two_bad_replies_go_to_manual_review(self):
        client = CountingClient(["bad", "worse"])
        label, status, attempts = classify(client, "p", "Found an insect")
        self.assertEqual((label["category"], status, client.calls), (MANUAL_REVIEW, "failed_validation", 2))
    def test_api_error_does_not_crash(self):
        class Boom:
            def generate(self, a, b): raise RuntimeError("quota")
        label, status, _ = classify(Boom(), "p", "Found an insect")
        self.assertEqual(label["category"], MANUAL_REVIEW)


class SafetyNetTests(unittest.TestCase):
    base = {"category": "other", "sentiment": "neutral", "urgent": False, "summary": "x"}
    def test_raises_urgent(self):
        new, raised = apply_safety_net("There was a cockroach in the curry", self.base)
        self.assertTrue(new["urgent"]); self.assertTrue(raised)
    def test_never_lowers_urgent(self):
        new, raised = apply_safety_net("Rice was undercooked", {**self.base, "urgent": True})
        self.assertTrue(new["urgent"]); self.assertFalse(raised)
    def test_tanglish_words(self):
        self.assertEqual(find_health_terms("Rasam la mudi irundhuchu"), ["mudi"])
        self.assertEqual(find_health_terms("Saapadu la poochi irundhuchu"), ["poochi"])
    def test_whole_word_only(self):
        self.assertEqual(find_health_terms("vaila vekka mudiyala"), [])
        self.assertEqual(find_health_terms("The chair was broken"), [])
    def test_taste_words_not_flagged(self):
        self.assertEqual(find_health_terms("Pongal had too much salt"), [])
        self.assertEqual(find_health_terms("Lemon rice was too sour"), [])


class CountingTests(unittest.TestCase):
    def test_counts_and_percent(self):
        res = [{"category": "taste", "sentiment": "negative"}, {"category": "taste", "sentiment": "positive"},
               {"category": "timing", "sentiment": "negative"}, {"category": MANUAL_REVIEW, "sentiment": MANUAL_REVIEW}]
        counts = count_by_category(res)
        self.assertEqual((counts["taste"], counts["timing"], counts["hygiene"], counts[MANUAL_REVIEW]), (2, 1, 0, 1))
        self.assertEqual(percent_negative(res), (2, 50.0))


class RecurringAndMealTimeTests(unittest.TestCase):
    def rows(self, *items):
        return [{"id": i, "meal": m, "comment": c} for i, m, c in items]
    def test_theme_needs_two_comments(self):
        one = self.rows(("F1", "Dinner", "Dinner was served 20 minutes late"))
        self.assertEqual(find_recurring_issues(one), [])
        two = one + self.rows(("F2", "Dinner", "Dinner started late again"))
        found = find_recurring_issues(two)
        self.assertEqual(found[0]["ids"], ["F1", "F2"])
    def test_late_lunch_batch_is_not_a_delay_complaint(self):
        r = self.rows(("F1", "Lunch", "Food ran out before the late lunch batch arrived"),
                      ("F2", "Dinner", "Dinner was served 20 minutes late"))
        self.assertFalse(any(i["theme"].startswith("Late") for i in find_recurring_issues(r)))
    SCHEDULE = {"dinner": {"meal": "Dinner", "scheduled_start": "19:30", "scheduled_end": "20:30", "serving_counter": "Counter 3"}}
    def test_no_delay_without_actual_time(self):
        text = meal_time_check({"meal": "Dinner", "comment": "Dinner was served 20 minutes late"}, self.SCHEDULE)
        self.assertIn("19:30 to 20:30", text); self.assertIn("no delay is calculated", text)
    def test_delay_when_clear_actual_time(self):
        self.assertEqual(find_actual_serving_time("Dinner started only at 8:15", "19:30"), "20:15")
        text = meal_time_check({"meal": "Dinner", "comment": "Dinner started only at 8:15"}, self.SCHEDULE)
        self.assertIn("45 minutes", text); self.assertIn("not verified", text)
    def test_unknown_meal(self):
        self.assertIn("no scheduled time", meal_time_check({"meal": "Snacks", "comment": "late"}, self.SCHEDULE))


if __name__ == "__main__":
    unittest.main()
