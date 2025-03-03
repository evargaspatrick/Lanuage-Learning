import speech_recognition as sr
import requests
import time
from gtts import gTTS
import playsound
import os
import unicodedata
from tempfile import NamedTemporaryFile

# DeepL API Key (replace with your actual key)
DEEPL_API_KEY = ''
DEEPL_URL = "https://api-free.deepl.com/v2/translate"

def translate_text(text, target_language):
    """
    Translate text to the target language using the DeepL API.
    """
    params = {
        'auth_key': DEEPL_API_KEY,
        'text': text,
        'target_lang': target_language
    }
    response = requests.post(DEEPL_URL, data=params)
    translation = response.json()['translations'][0]['text']
    return translation

def capture_user_voice():
    """
    Capture the user's voice and return the text.
    """
    recognizer = sr.Recognizer()
    
    # Adjust these settings for better recognition:
    # - phrase_time_limit: Maximum number of seconds for a phrase (None means no limit)
    # - pause_threshold: Seconds of non-speaking audio before a phrase is considered complete (default: 0.8)
    pause_threshold = 2.0  # Increase this to allow longer pauses between words
    
    with sr.Microphone() as source:
        print("Please say something...")
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = pause_threshold  # Set the pause threshold
        print("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=None)

    try:
        # Recognize speech using Google Speech Recognition
        print("Recognizing...")
        user_text = recognizer.recognize_google(audio)
        print(f"You said: {user_text}")
        return user_text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

def play_audio(text, language):
    """
    Convert the text into speech and play it.
    Uses a temporary file to avoid conflicts with previous plays.
    """
    try:
        # Create a temporary file with a unique name
        with NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        # Generate the speech and save to the temporary file
        tts = gTTS(text=text, lang=language)
        tts.save(temp_filename)
        
        # Add a small delay to ensure the file is properly written
        time.sleep(0.5)
        
        # Play the audio
        playsound.playsound(temp_filename)
        
        # Add a small delay before cleanup
        time.sleep(0.5)
    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
        # Clean up the temporary file if it exists
        try:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
        except Exception as e:
            print(f"Error cleaning up audio file: {e}")

def main():
    print("Welcome to the Language Learning App!")

    # Capture the sentence in the user's native language
    user_sentence = capture_user_voice()
    if not user_sentence:
        return

    print(f"You said: {user_sentence}")

    # Choose a target language (Spanish in this case)
    target_language = 'ES'  # You can change this to any supported language code

    # Translate the sentence
    translated_sentence = translate_text(user_sentence, target_language)
    print(f"Translation in {target_language}: {translated_sentence}")

    # Display original and translated sentences
    print("\nOriginal sentence:", user_sentence)
    print("Translation:", translated_sentence)

    # Ask if they want to be tested on the sentence
    test_choice = input("Do you want to be tested on saying this sentence? (yes/no): ").strip().lower()
    if test_choice == 'yes':
        while True:
            # Hide translation and prompt to say the sentence
            print("\nOkay, say the following sentence:")
            print(f"Say '{user_sentence}' in {target_language}.")

            # Play the sentence in the target language for the user to repeat
            play_audio(translated_sentence, target_language.lower())

            # Now, capture the user's attempt to say the sentence in the target language
            print("\nPlease say the sentence.")
            user_attempt = capture_user_voice()
            
            # Normalize text for comparison
            def normalize_text(text):
                if text is None:
                    return None
                # Convert to lowercase and normalize accents
                normalized = unicodedata.normalize('NFKD', text.lower())
                # Remove accents
                normalized = ''.join([c for c in normalized if not unicodedata.combining(c)])
                return normalized
                
            normalized_attempt = normalize_text(user_attempt)
            normalized_translation = normalize_text(translated_sentence)

            # Check if the user said the sentence correctly with normalized comparison
            if user_attempt and normalized_attempt == normalized_translation:
                print("Great job! You said the sentence correctly!")
                break
            else:
                print(f"Not quite right. The correct sentence is: {translated_sentence}")
                retry = input("Would you like to try again? (yes/no): ").strip().lower()
                if retry != 'yes':
                    print("Thanks for practicing!")
                    break

if __name__ == "__main__":
    main()
