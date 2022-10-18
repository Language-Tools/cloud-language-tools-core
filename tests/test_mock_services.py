import os
import sys
import logging
import unittest
import json
import pprint

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cloudlanguagetools
import cloudlanguagetools.servicemanager
from cloudlanguagetools.languages import Language
from cloudlanguagetools.constants import Service
import cloudlanguagetools.errors

def get_manager():
    manager = cloudlanguagetools.servicemanager.ServiceManager()
    manager.configure_default()
    return manager

class TestMockServices(unittest.TestCase):
    
    def test_language_data(self):
        if os.environ.get('CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES', 'no') != 'yes':
            return

        manager = get_manager()
        language_data = manager.get_language_data_json()
        self.assertTrue(len(language_data) > 0)


    def test_translation(self):
        if os.environ.get('CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES', 'no') != 'yes':
            return

        manager = get_manager()
        language_data = manager.get_language_data_json_v2()
        translation_options = language_data['free']['translation_options']
        # pprint.pprint(translation_options)
        translation_options_fr = [x for x in translation_options if x['language_code'] == 'fr']
        self.assertEqual(len(translation_options_fr), 1)

        translated_text_str = manager.get_translation('text_input', 'TestServiceA', 'fr', 'en')
        translated_text_obj = json.loads(translated_text_str)
        translated_text_expected = {
            'text': 'text_input',
            'from_language_key': 'fr',
            'to_language_key': 'en'
        }
        self.assertEqual(translated_text_obj, translated_text_expected)