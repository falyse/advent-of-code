from unittest import TestCase
import day_11


class TestDay11(TestCase):
    def test_increment(self):
        self.assertEqual(day_11.increment('aaa'), 'aab')
        self.assertEqual(day_11.increment('xz'), 'ya')
        self.assertEqual(day_11.increment('xzz'), 'yaa')

    def test_has_straight(self):
        self.assertEqual(day_11.has_straight('abc'), True)
        self.assertEqual(day_11.has_straight('xyz'), True)
        self.assertEqual(day_11.has_straight('xxabcxx'), True)
        self.assertEqual(day_11.has_straight('abd'), False)

    def test_num_pairs(self):
        self.assertEqual(day_11.num_pairs('aba'), 0)
        self.assertEqual(day_11.num_pairs('aa'), 1)
        self.assertEqual(day_11.num_pairs('aaa'), 1)
        self.assertEqual(day_11.num_pairs('aaaa'), 1)
        self.assertEqual(day_11.num_pairs('aabb'), 2)
