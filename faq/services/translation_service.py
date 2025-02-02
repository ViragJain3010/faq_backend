# from googletrans import Translator
# from bs4 import BeautifulSoup
# from typing import Dict, Optional
# import logging
# import time

# logger = logging.getLogger(__name__)

# class TranslationService:
#     def __init__(self):
#         self.translator = Translator()
#         self.supported_languages = ['hi', 'bn']
#         self.max_retries = 3
#         self.delay = 0.5  # delay between translations in seconds

#     def _is_language_supported(self, lang: str) -> bool:
#         return lang in self.supported_languages

#     def translate_text(self, text, lang):
#         """Translate plain text"""
#         translated = self.translator.translate(text, dest=lang)
#         return translated.text  # This will now return "Translated_lang_text"

#     # def translate_text(self, text: str, dest: str) -> Optional[str]:
#     #     if not text or dest == 'en' or not self._is_language_supported(dest):
#     #         return text
            
#     #     for attempt in range(self.max_retries):
#     #         try:
#     #             time.sleep(self.delay)
#     #             translation = self.translator.translate(text, dest=dest)
#     #             return translation.text
#     #         except Exception as e:
#     #             logger.error(f"Translation attempt {attempt + 1} failed: {str(e)}")
#     #             if attempt == self.max_retries - 1:
#     #                 logger.error(f"All translation attempts failed for text: {text}")
#     #                 return text

#     # def translate_html(self, html: str, dest: str) -> str:
#     #     """Translate HTML content while preserving tags"""
#     #     if not html or dest == 'en' or not self._is_language_supported(dest):
#     #         return html
        
#     #     try:
#     #         soup = BeautifulSoup(html, 'html.parser')
            
#     #         for element in soup.find_all(text=True):
#     #             if element.strip():
#     #                 translated_text = self.translate_text(element.string, dest)
#     #                 if translated_text:
#     #                     element.replace_with(translated_text)
            
#     #         return str(soup)
#     #     except Exception as e:
#     #         logger.error(f"HTML translation failed: {str(e)}")
#     #         return html

#     def translate_html(self, html, lang):
#         soup = BeautifulSoup(html, 'html.parser')
        
#         for element in soup.find_all(string=True):  # Note: Change text= to string=
#             if element.strip():
#                 translated = self.translate_text(element.strip(), lang)
#                 element.replace_with(translated)
                
#         return str(soup)

#     def translate_faq(self, question: str, answer: str) -> Dict[str, str]:
#         """Translate FAQ content to all supported languages"""
#         translations = {}
        
#         for lang in self.supported_languages:
#             try:
#                 translations[f'question_{lang}'] = self.translate_text(question, lang)
#                 translations[f'answer_{lang}'] = self.translate_html(answer, lang)
#             except Exception as e:
#                 logger.error(f"FAQ translation failed for {lang}: {str(e)}")
#                 translations[f'question_{lang}'] = ""
#                 translations[f'answer_{lang}'] = ""
        
#         return translations

from googletrans import Translator
from bs4 import BeautifulSoup
from typing import Dict


class TranslationService:
    def __init__(self):
        self.translator = Translator()
        self.supported_languages = ['hi', 'bn']

    def _is_language_supported(self, lang: str) -> bool:
        return lang in self.supported_languages

    def translate_text(self, text, lang):
        """Translate plain text"""
        translated = self.translator.translate(text, dest=lang)
        return translated.text 

    def translate_html(self, html, lang):
        soup = BeautifulSoup(html, 'html.parser')
        
        for element in soup.find_all(string=True): 
            if element.strip():
                translated = self.translate_text(element.strip(), lang)
                element.replace_with(translated)

        return str(soup)

    def translate_faq(self, question: str, answer: str) -> Dict[str, str]:
        """Translate FAQ content to all supported languages"""
        translations = {}
        
        for lang in self.supported_languages:
            try:
                # Translate question
                translated_question = self.translate_text(question, lang)
                if translated_question:
                    translations[f'question_{lang}'] = translated_question
                
                # Translate answer
                translated_answer = self.translate_html(answer, lang)
                if translated_answer:
                    translations[f'answer_{lang}'] = translated_answer
                else:
                    translations[f'answer_{lang}'] = answer
                    
            except Exception as e:
                translations[f'question_{lang}'] = question
                translations[f'answer_{lang}'] = answer
        
        return translations