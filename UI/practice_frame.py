import customtkinter as ctk
from tkinter import messagebox
from LearningTranslator import capture_user_voice, translate_text, play_audio, normalize_text, run_in_thread

class PracticeFrame:
    def __init__(self, parent, current_language):
        self.parent = parent
        self.current_language = current_language
        self.language_codes = {
            "Spanish": "ES", 
            "French": "FR", 
            "German": "DE", 
            "Japanese": "JA", 
            "Italian": "IT"
        }
        
    def create_frame(self, container):
        # Header frame to contain both title and status
        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)  # Left (title)
        header_frame.grid_columnconfigure(1, weight=1)  # Right (status)
        
        # Header - now in the header_frame instead of directly in container
        header = ctk.CTkLabel(
            header_frame, text=f"Translation Practice - {self.current_language.get()}", 
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="w"
        )
        header.grid(row=0, column=0, sticky="w")
        
        # Status label - now in the header_frame
        self.status_label = ctk.CTkLabel(
            header_frame, text="", 
            font=ctk.CTkFont(size=14),
            anchor="e"
        )
        self.status_label.grid(row=0, column=1, sticky="e")
        
        # Content frame - unchanged
        content_frame = ctk.CTkFrame(container)
        content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Voice input section
        input_frame = ctk.CTkFrame(content_frame)
        input_frame.pack(padx=20, pady=20, fill="x")
        
        input_label = ctk.CTkLabel(
            input_frame, text="Your Sentence:", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        input_label.pack(padx=20, pady=(20, 10), anchor="w")
        
        # Text display area
        self.input_text = ctk.CTkTextbox(input_frame, height=80)
        self.input_text.pack(padx=20, pady=10, fill="x")
        
        # Record button - modified to automatically translate after recording
        record_button = ctk.CTkButton(
            input_frame, text="Record Voice Input", 
            command=self.record_and_translate
        )
        record_button.pack(padx=20, pady=(10, 20))
        
        # Translation section
        translation_frame = ctk.CTkFrame(content_frame)
        translation_frame.pack(padx=20, pady=20, fill="x")
        
        translation_label = ctk.CTkLabel(
            translation_frame, text=f"Translation ({self.current_language.get()}):", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        translation_label.pack(padx=20, pady=(20, 10), anchor="w")
        
        # Translation display area
        self.translation_text = ctk.CTkTextbox(translation_frame, height=80)
        self.translation_text.pack(padx=20, pady=10, fill="x")
        
        # Repeat translation button - replaced the Play button
        repeat_button = ctk.CTkButton(
            translation_frame, text="Repeat Translation", 
            command=self.play_translation
        )
        repeat_button.pack(padx=20, pady=(10, 20), side="right")
        
        # Add a new section for practice mode
        practice_frame = ctk.CTkFrame(content_frame)
        practice_frame.pack(padx=20, pady=20, fill="x")
        
        practice_label = ctk.CTkLabel(
            practice_frame, text="Practice Mode:", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        practice_label.pack(padx=20, pady=(20, 10), anchor="w")
        
        # Start practice button
        self.practice_button = ctk.CTkButton(
            practice_frame, text="Start Practice Session", 
            command=self.start_practice
        )
        self.practice_button.pack(padx=20, pady=(10, 20))
        
        # Remove the old status frame at the bottom
        # self.status_frame = ctk.CTkFrame(content_frame, height=30)
        # self.status_frame.pack(padx=20, pady=(0, 10), fill="x", side="bottom")
        
        # self.status_label = ctk.CTkLabel(self.status_frame, text="")
        # self.status_label.pack(side="left", padx=10)
    
    def record_and_translate(self):
        """Record voice input and automatically translate it"""
        # Show a "Listening..." label
        self.show_status("Listening...")
        
        # Define callback functions
        @run_in_thread(self.on_voice_capture_complete)
        def threaded_capture_voice():
            return capture_user_voice()
        
        # Start the voice capture in a thread
        threaded_capture_voice()
    
    def on_voice_capture_complete(self, user_text):
        """Callback when voice capture completes"""
        # Update UI with speech recognition result
        if user_text:
            self.input_text.delete("0.0", "end")
            self.input_text.insert("0.0", user_text)
            
            # Update status
            self.show_status("Translating...")
            
            # Start translation in another thread
            @run_in_thread(self.on_translation_complete)
            def threaded_translate():
                lang_code = self.language_codes.get(self.current_language.get(), "ES")
                return translate_text(user_text, lang_code)
            
            # Start the translation thread
            threaded_translate()
        else:
            self.input_text.delete("0.0", "end")
            self.input_text.insert("0.0", "Could not recognize speech. Please try again.")
            self.show_status("")
    
    def on_translation_complete(self, translated_text):
        """Callback when translation completes"""
        self.translation_text.delete("0.0", "end")
        self.translation_text.insert("0.0", translated_text)
        self.show_status("")
        
        # Play the translation in a thread
        self.play_translation()
    
    def translate_text(self):
        """Manual translation function (kept for direct text input)"""
        input_text = self.input_text.get("0.0", "end").strip()
        if input_text:
            lang_code = self.language_codes.get(self.current_language.get(), "ES")
            translated_text = translate_text(input_text, lang_code)
            
            self.translation_text.delete("0.0", "end")
            self.translation_text.insert("0.0", translated_text)
            
            # Automatically play the translation
            self.play_translation()
        else:
            self.translation_text.delete("0.0", "end")
            self.translation_text.insert("0.0", "Please enter or record text to translate first.")
    
    def play_translation(self):
        """Play the current translation"""
        translation = self.translation_text.get("0.0", "end").strip()
        if translation:
            self.show_status("Playing audio...")
            
            @run_in_thread(lambda result: self.show_status(""))
            def threaded_play_audio():
                lang_code = self.language_codes.get(self.current_language.get(), "es").lower()
                play_audio(translation, lang_code)
            
            threaded_play_audio()
    
    def start_practice(self):
        # Get the current text
        original_text = self.input_text.get("0.0", "end").strip()
        translated_text = self.translation_text.get("0.0", "end").strip()
        
        if not original_text or not translated_text:
            # Show error if no text to practice
            messagebox.showwarning("Practice Error", "Please enter and translate text first")
            return
        
        # Create a new window for practice
        practice_window = ctk.CTkToplevel(self.parent)
        practice_window.title("Translation Practice")
        practice_window.geometry("600x400")
        practice_window.grab_set()  # Make window modal
        
        # Original sentence frame
        original_frame = ctk.CTkFrame(practice_window)
        original_frame.pack(padx=20, pady=20, fill="x")
        
        original_label = ctk.CTkLabel(
            original_frame, 
            text=f"Say this sentence in {self.current_language.get()}:", 
            font=ctk.CTkFont(size=14)
        )
        original_label.pack(padx=20, pady=10, anchor="w")
        
        sentence_label = ctk.CTkLabel(
            original_frame, text=original_text, 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        sentence_label.pack(padx=20, pady=10)
        
        # Auto-play the translation when practice starts
        self.parent.after(500, lambda: self.play_practice_audio(translated_text))
        
        # Listen button renamed to Repeat Translation
        listen_button = ctk.CTkButton(
            original_frame, text="Repeat Translation", 
            command=lambda: self.play_practice_audio(translated_text)
        )
        listen_button.pack(padx=20, pady=10)
        
        # Attempt frame
        attempt_frame = ctk.CTkFrame(practice_window)
        attempt_frame.pack(padx=20, pady=20, fill="x")
        
        # Record attempt button
        record_button = ctk.CTkButton(
            attempt_frame, text="Record Your Attempt", 
            command=lambda: self.record_practice_attempt(practice_window, translated_text)
        )
        record_button.pack(padx=20, pady=20)
        
        # Result label
        self.result_label = ctk.CTkLabel(
            attempt_frame, text="", 
            font=ctk.CTkFont(size=14)
        )
        self.result_label.pack(padx=20, pady=10)
    
    def play_practice_audio(self, text):
        """Play the translation audio with improved threading and error handling"""
        # Use the language code for the selected language
        lang_code = self.language_codes.get(self.current_language.get(), "es").lower()
        self.show_status(f"Playing {self.current_language.get()} audio...")
        
        @run_in_thread(lambda result: self.show_status(""))
        def threaded_play_audio():
            # Debug output in thread
            print(f"Starting audio playback for language: {lang_code}")
            # Call the play_audio function
            play_audio(text, lang_code)
            # Return any value to trigger the callback
            return True
        
        # Start the audio playback in a separate thread
        threaded_play_audio()
    
    def record_practice_attempt(self, window, target_text):
        # Show status
        self.result_label.configure(text="Listening...")
        
        @run_in_thread(lambda result: self.process_practice_attempt(result, target_text))
        def threaded_capture_voice():
            return capture_user_voice()
        
        threaded_capture_voice()
    
    def process_practice_attempt(self, user_attempt, target_text):
        if not user_attempt:
            self.result_label.configure(text="Could not recognize your speech. Please try again.")
            return
        
        # Normalize both texts for comparison
        normalized_attempt = normalize_text(user_attempt)
        normalized_target = normalize_text(target_text)
        
        # Check if the attempt matches the translation
        if normalized_attempt == normalized_target:
            self.result_label.configure(text="Great job! You said the sentence correctly!")
        else:
            self.result_label.configure(text=f"Not quite right.\nYou said: {user_attempt}\nCorrect: {target_text}")
    
    def show_status(self, message):
        """Show a status message in the header bar"""
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=message)
            self.parent.update_idletasks()  # Force update the UI