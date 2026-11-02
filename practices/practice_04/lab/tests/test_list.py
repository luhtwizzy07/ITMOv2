import unittest

import service


class ListSubscribersTest(unittest.TestCase):
    def setUp(self):
        service.subscribers.clear()

    def listing(self):
        self.assertTrue(hasattr(service, "list_subscribers"), "feature A is missing")
        return service.list_subscribers()

    def test_empty(self):
        self.assertEqual(self.listing(), [])

    def test_sorted_trimmed_unique(self):
        for name in (" Zoe ", "Ann", "Bob", "Ann"):
            service.subscribe(name)
        self.assertEqual(self.listing(), ["Ann", "Bob", "Zoe"])

    def test_returned_list_does_not_mutate_storage(self):
        service.subscribe("Ann")
        result = self.listing()
        result.append("Intruder")
        result.remove("Ann")
        self.assertEqual(self.listing(), ["Ann"])

    def test_snapshot_and_later_subscription(self):
        service.subscribe("Ann")
        snapshot = self.listing()
        service.subscribe("Bob")
        self.assertEqual(snapshot, ["Ann"])
        self.assertEqual(self.listing(), ["Ann", "Bob"])

    def test_case_sensitive_order(self):
        for name in ("bob", "ann", "Ann"):
            service.subscribe(name)
        self.assertEqual(self.listing(), ["Ann", "ann", "bob"])
