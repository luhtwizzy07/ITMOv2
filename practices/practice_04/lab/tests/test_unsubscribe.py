import unittest

import service


class UnsubscribeTest(unittest.TestCase):
    def setUp(self):
        service.subscribers.clear()

    def remove(self, name):
        self.assertTrue(hasattr(service, "unsubscribe"), "feature B is missing")
        return service.unsubscribe(name)

    def test_existing_name(self):
        service.subscribe("Ann")
        self.assertEqual(self.remove("Ann"), {"unsubscribed": True})
        self.assertEqual(service.list_subscribers(), [])

    def test_missing_name(self):
        service.subscribe("Ann")
        self.assertEqual(self.remove("Bob"), {"unsubscribed": False})
        self.assertEqual(service.list_subscribers(), ["Ann"])

    def test_repeated_removal(self):
        service.subscribe("Ann")
        self.assertEqual(self.remove("Ann"), {"unsubscribed": True})
        self.assertEqual(self.remove("Ann"), {"unsubscribed": False})

    def test_trimmed_name(self):
        service.subscribe(" Ann ")
        self.assertEqual(self.remove(" Ann "), {"unsubscribed": True})
        self.assertEqual(service.list_subscribers(), [])

    def test_empty_name_preserves_state(self):
        service.subscribe("Ann")
        self.assertTrue(hasattr(service, "unsubscribe"), "feature B is missing")
        for name in ("", " ", "\t\n"):
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError, "empty name"):
                    service.unsubscribe(name)
                self.assertEqual(service.list_subscribers(), ["Ann"])

    def test_other_subscribers_are_preserved(self):
        service.subscribe("Ann")
        service.subscribe("Bob")
        self.assertEqual(self.remove("Ann"), {"unsubscribed": True})
        self.assertEqual(service.list_subscribers(), ["Bob"])

    def test_names_remain_case_sensitive(self):
        service.subscribe("Ann")
        self.assertEqual(self.remove("ann"), {"unsubscribed": False})
        self.assertEqual(service.list_subscribers(), ["Ann"])

    def test_subscribe_after_removal(self):
        service.subscribe("Ann")
        self.remove("Ann")
        self.assertEqual(service.subscribe("Ann"), {"subscribed": True})
        self.assertEqual(service.list_subscribers(), ["Ann"])
