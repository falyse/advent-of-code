from unittest import TestCase
from day_05 import has_repeated_pair

class Test_has_repeated_pair(TestCase):
    def test_has_repeated_pair(self):
        self.assertEqual(has_repeated_pair('xyxy'), True)
        self.assertEqual(has_repeated_pair('aabcdefgaa'), True)
        self.assertEqual(has_repeated_pair('aaa'), False)
        self.assertEqual(has_repeated_pair('asdfooaooaa'), True)
