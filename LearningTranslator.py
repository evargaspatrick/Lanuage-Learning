import speech_recognition as sr
import requests
import time
from gtts import gTTS
import playsound
import os
import unicodedata
from tempfile import NamedTemporaryFile
from utility.config_manager import get_api_key
import threading
from functools import partial

# DeepL API Key
DEEPL_API_KEY = get_api_key()
DEEPL_URL = "https://api-free.deepl.com/v2/translate"

def translate_text(text, target_language):
    """
    Translate text to the target language using the DeepL API.
    """
    # Check if API key is set
    if not DEEPL_API_KEY:
        print("Error: DeepL API key is not configured.")
        return f"[Translation Error: API key not configured. Please set your DeepL API key.]"
    
    params = {
        'auth_key': DEEPL_API_KEY,
        'text': text,
        'target_lang': target_language
    }
    
    try:
        response = requests.post(DEEPL_URL, data=params, timeout=10)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Try to parse the JSON response
        try:
            data = response.json()
            if 'translations' in data and len(data['translations']) > 0:
                return data['translations'][0]['text']
            else:
                print(f"Unexpected API response format: {data}")
                return f"[Translation Error: Unexpected API response format]"
        except requests.exceptions.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response content: {response.text}")
            return f"[Translation Error: Invalid response from API]"
            
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return f"[Translation Error: Could not connect to translation service]"

def capture_user_voice():
    """
    Capture the user's voice and return the text.
    Improved to handle longer phrases better.
    """
    recognizer = sr.Recognizer()
    
    # Adjust these parameters for better recognition of longer sentences
    recognizer.pause_threshold = 3.0  # Longer pause threshold (seconds)
    recognizer.phrase_threshold = 0.3  # Lower phrase threshold for better continuous recognition
    recognizer.non_speaking_duration = 1.0  # Longer duration for non-speaking
    
    with sr.Microphone() as source:
        print("Please say something...")
        # Adjust for ambient noise with longer duration
        recognizer.adjust_for_ambient_noise(source, duration=1.0)
        print("Listening...")
        
        try:
            # Set a longer timeout to wait for speech to start
            # Set a longer phrase_time_limit for longer phrases
            audio = recognizer.listen(
                source, 
                timeout=10.0,  # Wait up to 10 seconds for speech to start
                phrase_time_limit=10.0  # Allow phrases up to 10 seconds long
            )
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period")
            return None

    try:
        print("Recognizing...")
        # Use a more robust recognition setting
        user_text = recognizer.recognize_google(
            audio, 
            language="en-US",  # Explicitly set language
            show_all=False     # Return best match
        )
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
    Uses pygame as the primary audio player with proper resource management.
    """
    import os
    import tempfile
    import time
    
    # Print debug info
    print(f"Playing audio in language: {language}")
    print(f"Text to speak: {text[:30]}{'...' if len(text) > 30 else ''}")
    
    temp_filename = None
    
    try:
        # Create a temporary file with a valid filename
        temp_dir = tempfile.gettempdir()
        temp_filename = os.path.join(temp_dir, f"speech_{int(time.time())}.mp3")
        print(f"Creating temp file: {temp_filename}")
        
        # Generate the speech
        tts = gTTS(text=text, lang=language)
        tts.save(temp_filename)
        
        # Wait for file to be ready
        time.sleep(0.5)
        print("Audio file created successfully")
        
        # Use pygame as the primary audio player
        try:
            import pygame
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            
            print("Loading audio with pygame...")
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            
            print("Playing audio...")
            # Wait for playback to finish with a timeout
            start_time = time.time()
            timeout = 30  # Maximum wait time in seconds
            
            while pygame.mixer.music.get_busy() and (time.time() - start_time < timeout):
                pygame.time.Clock().tick(10)  # Limit the loop to 10 times per second
            
            # Make sure we stop playback if we're exiting the loop due to timeout
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                print("Audio playback timed out")
            else:
                print("Audio playback completed")
            
        except Exception as pygame_error:
            print(f"Pygame error: {pygame_error}")
            # Fallback to playsound with non-blocking mode
            try:
                print("Falling back to playsound...")
                playsound.playsound(temp_filename, False)  # Non-blocking
                # Give it time to play
                time.sleep(5)  # Adjust based on typical audio length
            except Exception as playsound_error:
                print(f"Playsound error: {playsound_error}")
                print("All audio playback methods failed")
            
    except Exception as e:
        print(f"Error in play_audio: {e}")
    finally:
        # Clean up with a delay to ensure file is no longer in use
        if temp_filename and os.path.exists(temp_filename):
            try:
                print(f"Attempting to remove temp file: {temp_filename}")
                # Wait a moment before deleting
                time.sleep(2.0)
                os.remove(temp_filename)
                print("Temp file removed successfully")
            except Exception as e:
                print(f"Error removing temporary file: {e}")
                # Schedule removal for later in a separate thread
                def delayed_remove():
                    try:
                        time.sleep(5)
                        if os.path.exists(temp_filename):
                            os.remove(temp_filename)
                            print("Temp file removed with delay")
                    except Exception as delayed_error:
                        print(f"Failed to remove temp file with delay: {delayed_error}")
                
                threading.Thread(target=delayed_remove).start()

def normalize_text(text):
    """
    Normalize text by removing accents and converting to lowercase
    for better comparison.
    """
    if text is None:
        return None
    # Convert to lowercase and normalize accents
    normalized = unicodedata.normalize('NFKD', text.lower())
    # Remove accents
    normalized = ''.join([c for c in normalized if not unicodedata.combining(c)])
    return normalized

def run_in_thread(callback=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if callback:
                def thread_target():
                    result = func(*args, **kwargs)
                    callback(result)
                threading.Thread(target=thread_target).start()
                return None
            else:
                threading.Thread(target=partial(func, *args, **kwargs)).start()
                return None
        return wrapper
    return decorator

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
