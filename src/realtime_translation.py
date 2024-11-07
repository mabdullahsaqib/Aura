from googletrans import Translator

# Initialize the translator
translator = Translator()


def translate_text(text, target_language="en"):
    """
    Translates text to a specified target language.

    Parameters:
        text (str): The text to translate.
        target_language (str): The language code to translate the text to (e.g., "en" for English, "fr" for French).

    Returns:
        str: The translated text.
    """
    try:
        # Detect the original language
        detected_language = translator.detect(text).lang
        print(f"Detected language: {detected_language}")

        # Translate the text to the target language
        translated = translator.translate(text, dest=target_language)
        print(f"Translated to {target_language}: {translated.text}")

        return translated.text

    except Exception as e:
        print(f"Error during translation: {e}")
        return None


# Example Usage
if __name__ == "__main__":
    # Translate text from French to English
    original_text = "Aap sab kaise ho?"
    translated_text = translate_text(original_text, "en")
    print(f"Original: {original_text}")
    print(f"Translated: {translated_text}")
