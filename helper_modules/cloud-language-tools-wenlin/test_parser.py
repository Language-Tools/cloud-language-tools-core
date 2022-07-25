import unittest
import clt_wenlin


class TestWenlinParser(unittest.TestCase):
    def test_process_characters(self):
        input = '阿拉伯半岛[----島]'
        simplified, traditional = clt_wenlin.process_characters(input)
        self.assertEqual(simplified, '阿拉伯半岛')
        self.assertEqual(traditional, '阿拉伯半島')

        input = '按例'
        simplified, traditional = clt_wenlin.process_characters(input)
        self.assertEqual(simplified, '按例')
        self.assertEqual(traditional, '按例')

        input = '按铃儿[-鈴兒]'
        simplified, traditional = clt_wenlin.process_characters(input)
        self.assertEqual(simplified, '按铃儿')
        self.assertEqual(traditional, '按鈴兒')  