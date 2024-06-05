from deep_translator import GoogleTranslator

# Function to translate text from one language to another
def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translation = translator.translate(text)
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        translation = ""
    return translation