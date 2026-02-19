from deep_translator import GoogleTranslator
from typing import List, Union

class TranslationService:
    def __init__(self):
        # Default languages for WikiKisan
        self.supported_langs = ['en', 'hi', 'te']

    async def translate_text(self, text: str, target_lang: str = 'en') -> str:
        """
        Translates a single string into the target language.
        """
        try:
            if target_lang not in self.supported_langs:
                return text
                
            translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
            return translated
        except Exception as e:
            print(f"Translation Error: {e}")
            return text

    async def translate_batch(self, texts: List[str], target_lang: str) -> List[str]:
        """
        Translates a list of strings efficiently.
        """
        translator = GoogleTranslator(source='auto', target=target_lang)
        return [translator.translate(t) for t in texts]

# Global instance
translator = TranslationService()
