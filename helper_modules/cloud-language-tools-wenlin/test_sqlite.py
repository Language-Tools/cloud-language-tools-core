import unittest
import clt_wenlin
import tempfile
import sqlite3
import json


class TestWenlinSqlite(unittest.TestCase):
    def test_create_sqlite_file(self):
        dictionary_filepath = '/home/luc/cpp/wenlin/server/cidian.u8'
        sqlite_tempfile = tempfile.NamedTemporaryFile(suffix='.db')

        clt_wenlin.create_sqlite_file(dictionary_filepath, sqlite_tempfile.name)

        # try to query the file
        connection = sqlite3.connect(sqlite_tempfile.name)
        cur = connection.cursor()

        # lookup by chinese characters
        # ============================

        query = """SELECT entry, entry_id FROM words WHERE simplified='啊'"""
        results = []
        for row in cur.execute(query):
            results.append(row)

        self.assertEqual(len(results), 5)

        # check entry_id
        self.assertEqual(results[0][1], 1000000063)

        entry_json_str = results[0][0]
        entry_dict = json.loads(entry_json_str)

        expected_entry_dict = {'parts_of_speech': [
                                    {'definitions': [
                                                {'definition': 'used as phrase suffix'},
                                                {'definition': 'in enumeration',
                                                'example_chinese': '钱∼, 书∼, 表∼, 我都丢了。',
                                                'example_pinyin': 'Qián ∼, shū ∼, biǎo '
                                                                    '∼, wǒ dōu diū le.',
                                                'example_translation': 'Money, books, '
                                                                        'watch, I lost '
                                                                        'everything.'},
                                                {'definition': 'in direct address and '
                                                                'exclamation',
                                                'example_chinese': '老王∼, 这可不行∼!',
                                                'example_pinyin': 'Lǎo Wáng ∼, zhè kě '
                                                                    'bùxíng ∼!',
                                                'example_translation': 'Wang, this '
                                                                        "won't do!"},
                                                {'definition': 'indicating '
                                                                'obviousness/impatience',
                                                'example_chinese': '来∼!',
                                                'example_pinyin': 'Lái ∼!',
                                                'example_translation': 'Come on!'},
                                                {'definition': 'for confirmation',
                                                'example_chinese': '你不来∼?',
                                                'example_pinyin': 'Nǐ bù lái ∼?',
                                                'example_translation': "So you're not "
                                                                        'coming?'}],
                                            'part_of_speech': 'm.p.'}
                                        ],
        'simplified': '啊',
        'traditional': '啊',
        'pinyin': 'a*'}        

        self.maxDiff = None
        self.assertEqual(entry_dict, expected_entry_dict)

        # lookup by definitions
        # =====================

        query = """SELECT definition, entry_id FROM definitions WHERE definitions MATCH 'confirmation'"""
        results = []
        for row in cur.execute(query):
            print(row)
            results.append(row)        

        expected_results = [
            ('for confirmation', 1000000063),
            ('confirmation', 1000344607),
            ('wait in prison (for confirmation of death sentence)', 1005750902),
            ('confirmation', 1005838396),
            ('empirical confirmation', 1006395370),
            ('seek confirmation', 1010373340),
            ('letter of confirmation; confirming order; confirmation note', 1010507879),
            ("be subject to one's confirmation", 1010507976),
            ('confirmation of an oracle', 1017161691),
            ('confirmation; definite note', 1018032266)
        ]

        self.assertEqual(results, expected_results)




