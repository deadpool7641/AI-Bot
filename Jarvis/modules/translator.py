from deep_translator import GoogleTranslator
from langdetect import detect


def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"


def translate_to(text, target_lang):
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except:
        return text
