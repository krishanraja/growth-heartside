import unittest

import growth


class HostNameTests(unittest.TestCase):
    def test_new_host_and_customer_dog_names_are_distinct(self):
        for text in ('Buddy: Tell me about your dog.', 'Love, Biscuit'):
            self.assertFalse(any('retired host' in p for p in growth.problems({'platform': 'instagram', 'text': text})))

    def test_retired_host_is_rejected_in_public_and_script_copy(self):
        for platform in ('instagram', 'script'):
            for text in ('Biscuit: Tell me about your dog.', 'Tell Biscuit about your dog.'):
                self.assertTrue(any('retired host' in p for p in growth.problems({'platform': platform, 'text': text})))
