import customtkinter as ctk
from tkinter import messagebox
from LearningTranslator import capture_user_voice, play_audio, normalize_text, run_in_thread

class EnunciationFrame:
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
        
        # Common phrases for practice (starter set)
        self.practice_phrases = {
            "Spanish": [
                "Buenos días, ¿cómo estás?",
                "Me gustaría un café, por favor",
                "¿Dónde está la estación de tren?",
                "Muchas gracias por tu ayuda",
                "¿Qué hora es?",
                "La comida está muy rica"
            ],
            "French": [
                "Bonjour, comment allez-vous?",
                "Je voudrais un café, s'il vous plaît",
                "Où est la gare?",
                "Merci beaucoup pour votre aide",
                "Quelle heure est-il?",
                "La nourriture est très bonne"
            ],
            "German": [
                "Guten Tag, wie geht es Ihnen?",
                "Ich hätte gerne einen Kaffee, bitte",
                "Wo ist der Bahnhof?",
                "Vielen Dank für Ihre Hilfe",
                "Wie spät ist es?",
                "Das Essen ist sehr lecker"
            ],
            "Italian": [
                "Buongiorno, come stai?",
                "Vorrei un caffè, per favore",
                "Dov'è la stazione ferroviaria?",
                "Grazie mille per il tuo aiuto",
                "Che ora è?",
                "Il cibo è molto buono"
            ],
            "Japanese": [
                "こんにちは、お元気ですか？",
                "コーヒーをください",
                "駅はどこですか？",
                "ご協力ありがとうございます",
                "今何時ですか？",
                "食べ物はとても美味しいです"
            ]
        }
        
        self.current_phrase_index = 0
        
    def create_frame(self, container):
        # Header frame with title and status
        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        header = ctk.CTkLabel(
            header_frame, text=f"Enunciation Practice - {self.current_language.get()}", 
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="w"
        )
        header.grid(row=0, column=0, sticky="w")
        
        # Status label
        self.status_label = ctk.CTkLabel(
            header_frame, text="", 
            font=ctk.CTkFont(size=14),
            anchor="e"
        )
        self.status_label.grid(row=0, column=1, sticky="e")
        
        # Main content
        content_frame = ctk.CTkFrame(container)
        content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        # Introduction text
        intro_text = ctk.CTkLabel(
            content_frame,
            text="Practice your pronunciation with common phrases.",
            font=ctk.CTkFont(size=16)
        )
        intro_text.pack(padx=20, pady=20)
        
        # Phrase display frame
        phrase_frame = ctk.CTkFrame(content_frame)
        phrase_frame.pack(padx=20, pady=20, fill="x")
        
        # Current phrase display
        phrase_label = ctk.CTkLabel(
            phrase_frame, 
            text="Current Phrase:", 
            font=ctk.CTkFont(size=14)
        )
        phrase_label.pack(padx=20, pady=(20, 5), anchor="w")
        
        self.phrase_display = ctk.CTkLabel(
            phrase_frame,
            text=self.get_current_phrase(),
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.phrase_display.pack(padx=20, pady=10)
        
        # Listen button
        listen_button = ctk.CTkButton(
            phrase_frame,
            text="Listen to Phrase",
            command=self.play_current_phrase
        )
        listen_button.pack(padx=20, pady=10)
        
        # Practice section
        practice_frame = ctk.CTkFrame(content_frame)
        practice_frame.pack(padx=20, pady=20, fill="x")
        
        practice_label = ctk.CTkLabel(
            practice_frame,
            text="Your Turn:",
            font=ctk.CTkFont(size=14)
        )
        practice_label.pack(padx=20, pady=(20, 10), anchor="w")
        
        # Record button
        record_button = ctk.CTkButton(
            practice_frame,
            text="Record Your Pronunciation",
            command=self.record_pronunciation
        )
        record_button.pack(padx=20, pady=10)
        
        # Feedback display
        self.feedback_label = ctk.CTkLabel(
            practice_frame,
            text="",
            font=ctk.CTkFont(size=14),
            wraplength=500
        )
        self.feedback_label.pack(padx=20, pady=10)
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        nav_frame.pack(padx=20, pady=20, fill="x")
        
        prev_button = ctk.CTkButton(
            nav_frame,
            text="← Previous Phrase",
            command=self.previous_phrase,
            width=150
        )
        prev_button.pack(side="left", padx=20)
        
        next_button = ctk.CTkButton(
            nav_frame,
            text="Next Phrase →",
            command=self.next_phrase,
            width=150
        )
        next_button.pack(side="right", padx=20)
    
    def get_current_phrase(self):
        """Get the current phrase based on the selected language"""
        language = self.current_language.get()
        phrases = self.practice_phrases.get(language, [])
        
        if not phrases:
            return "No phrases available for this language"
        
        if self.current_phrase_index >= len(phrases):
            self.current_phrase_index = 0
            
        return phrases[self.current_phrase_index]
    
    def play_current_phrase(self):
        """Play the audio for the current phrase"""
        phrase = self.get_current_phrase()
        lang_code = self.language_codes.get(self.current_language.get(), "es").lower()
        
        self.show_status(f"Playing {self.current_language.get()} audio...")
        
        @run_in_thread(lambda result: self.show_status(""))
        def threaded_play_audio():
            play_audio(phrase, lang_code)
            return True
        
        threaded_play_audio()
    
    def record_pronunciation(self):
        """Record the user's pronunciation and check it"""
        self.feedback_label.configure(text="Listening...")
        
        @run_in_thread(self.process_pronunciation)
        def threaded_capture_voice():
            return capture_user_voice()
        
        threaded_capture_voice()
    
    def process_pronunciation(self, user_audio):
        """Process the user's pronunciation and provide feedback"""
        if not user_audio:
            self.feedback_label.configure(text="Could not detect speech. Please try again.")
            return
        
        # Get the current phrase
        current_phrase = self.get_current_phrase()
        
        # Normalize both texts for comparison
        normalized_user = normalize_text(user_audio)
        normalized_phrase = normalize_text(current_phrase)
        
        # Use exact matching like in practice_frame.py
        if normalized_user == normalized_phrase:
            self.feedback_label.configure(
                text=f"Excellent pronunciation!\nYou said: {user_audio}"
            )
        else:
            # If not exact match, still provide similarity score for feedback
            similarity = self.calculate_similarity(normalized_user, normalized_phrase)
            
            if similarity > 0.7:
                self.feedback_label.configure(
                    text=f"Good attempt! ({similarity:.0%} match)\nYou said: {user_audio}\nCorrect: {current_phrase}"
                )
            else:
                self.feedback_label.configure(
                    text=f"Keep practicing!\nYou said: {user_audio}\nCorrect: {current_phrase}"
                )
    
    def calculate_similarity(self, text1, text2):
        """Calculate a simple similarity score between two texts"""
        if not text1 or not text2:
            return 0.0
            
        # Convert to sets of words for comparison
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        # Calculate Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        if union == 0:
            return 0.0
            
        return intersection / union
    
    def next_phrase(self):
        """Go to the next practice phrase"""
        language = self.current_language.get()
        phrases = self.practice_phrases.get(language, [])
        
        if not phrases:
            return
            
        self.current_phrase_index = (self.current_phrase_index + 1) % len(phrases)
        self.phrase_display.configure(text=self.get_current_phrase())
        self.feedback_label.configure(text="")
    
    def previous_phrase(self):
        """Go to the previous practice phrase"""
        language = self.current_language.get()
        phrases = self.practice_phrases.get(language, [])
        
        if not phrases:
            return
            
        self.current_phrase_index = (self.current_phrase_index - 1) % len(phrases)
        self.phrase_display.configure(text=self.get_current_phrase())
        self.feedback_label.configure(text="")
    
    def show_status(self, message):
        """Update the status label"""
        self.status_label.configure(text=message)
        self.parent.update_idletasks()