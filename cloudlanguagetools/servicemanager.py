import os
import base64
import tempfile
import cloudlanguagetools.constants
import cloudlanguagetools.azure
import cloudlanguagetools.google
import cloudlanguagetools.mandarincantonese

class ServiceManager():
    def  __init__(self):
        self.services = {}
        self.services[cloudlanguagetools.constants.Service.Azure.name] = cloudlanguagetools.azure.AzureService()
        self.services[cloudlanguagetools.constants.Service.Google.name] = cloudlanguagetools.google.GoogleService()
        self.services[cloudlanguagetools.constants.Service.MandarinCantonese.name] = cloudlanguagetools.mandarincantonese.MandarinCantoneseService()

    def configure(self):
        # azure
        self.configure_azure(os.environ['AZURE_REGION'], os.environ['AZURE_KEY'], os.environ['AZURE_TRANSLATOR_KEY'])

        # google
        google_key = os.environ['GOOGLE_KEY']
        data_bytes = base64.b64decode(google_key)
        data_str = data_bytes.decode('utf-8')    
        # write to file
        # note: temp file needs to be a member so it doesn't get collected
        self.google_key_temp_file = tempfile.NamedTemporaryFile()  
        google_key_filename = self.google_key_temp_file.name
        with open(google_key_filename, 'w') as f:
            f.write(data_str)    
            f.close()
        self.configure_google(google_key_filename)

        self.translation_language_list = self.get_translation_language_list()

    def configure_azure(self, region, key, translator_key):
        self.services[cloudlanguagetools.constants.Service.Azure.name].configure(key, region, translator_key)

    def configure_google(self, credentials_path):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        self.services[cloudlanguagetools.constants.Service.Google.name].configure()

    def get_language_list(self):
        result_dict = {}
        for language in cloudlanguagetools.constants.Language:
            result_dict[language.name] = language.lang_name
        return result_dict

    def get_tts_voice_list(self):
        result = []
        for key, service in self.services.items():
            result.extend(service.get_tts_voice_list())
        return result

    def get_tts_voice_list_json(self):
        tts_voice_list = self.get_tts_voice_list()
        return [voice.json_obj() for voice in tts_voice_list]

    def get_translation_language_list(self):
        result = []
        for key, service in self.services.items():
            result.extend(service.get_translation_language_list())
        return result        

    def get_translation_language_list_json(self):
        """return list of languages supported for translation, using plain objects/strings"""
        language_list = self.get_translation_language_list()
        return [language.json_obj() for language in language_list]

    def get_transliteration_language_list(self):
        result = []
        for key, service in self.services.items():
            result.extend(service.get_transliteration_language_list())
        return result

    def get_transliteration_language_list_json(self):
        """return list of languages supported for transliteration, using plain objects/strings"""
        language_list = self.get_transliteration_language_list()
        return [language.json_obj() for language in language_list]

    def get_tts_audio(self, text, service, voice_id, options):
        service = self.services[service]
        return service.get_tts_audio(text, voice_id, options)

    def get_translation(self, text, service, from_language_key, to_language_key):
        """return text"""
        service = self.services[service]
        return service.get_translation(text, from_language_key, to_language_key)

    def get_all_translations(self, text, from_language, to_language):
        result = {}
        for service_name, service in self.services.items():
            # locate from language key
            from_language_entries = [x for x in self.translation_language_list if x.service.name == service_name and x.get_language_code() == from_language]
            if len(from_language_entries) == 1:
                # this service provides the "from" language in translation list
                from_language_id = from_language_entries[0].get_language_id()
                # locate to language key
                to_language_entries = [x for x in self.translation_language_list if x.service.name == service_name and x.get_language_code() == to_language]
                assert(len(to_language_entries) == 1)
                to_language_id = to_language_entries[0].get_language_id()
                result[service_name] = self.get_translation(text, service_name, from_language_id, to_language_id)
        return result

    def get_transliteration(self, text, service, transliteration_key):
        service = self.services[service]
        return service.get_transliteration(text, transliteration_key)

    def detect_language(self, text_list):
        """returns an enum from constants.Language"""
        service = self.services[cloudlanguagetools.constants.Service.Azure.name]
        result = service.detect_language(text_list)
        return result