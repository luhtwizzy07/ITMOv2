import unittest

from service import subscribe, subscribers


class SubscribeTest(unittest.TestCase):
    def setUp(self):
        subscribers.clear()

    def test_subscribe(self):
        self.assertEqual(subscribe("Ann"), {"subscribed": True})
        self.assertEqual(subscribers, {"Ann"})

    def test_empty(self):
        with self.assertRaisesRegex(ValueError, "empty name"):
            subscribe(" ")
        self.assertEqual(subscribers, set())

    def test_duplicate(self):
        subscribe("Ann")
        subscribe("Ann")
        self.assertEqual(len(subscribers), 1)

    def test_trim(self):
        subscribe(" Ann ")
        self.assertEqual(subscribers, {"Ann"})
