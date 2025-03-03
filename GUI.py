import customtkinter as ctk
import os
from PIL import Image
import random

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class LanguageLearningApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Linguify - Modern Language Learning")
        self.geometry("1100x700")
        self.minsize(800, 600)
        
        # Create variables
        self.current_language = ctk.StringVar(value="Spanish")
        self.current_page = "dashboard"
        self.languages = ["Spanish", "French", "German", "Japanese", "Italian"]
        self.progress = {lang: random.randint(0, 100) for lang in self.languages}
        
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # Sidebar elements
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="Linguify", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.dashboard_button = ctk.CTkButton(
            self.sidebar_frame, text="Dashboard", 
            command=self.show_dashboard, fg_color="transparent", 
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w"
        )
        self.dashboard_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.lessons_button = ctk.CTkButton(
            self.sidebar_frame, text="Lessons", 
            command=self.show_lessons, fg_color="transparent", 
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w"
        )
        self.lessons_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.practice_button = ctk.CTkButton(
            self.sidebar_frame, text="Practice", 
            command=self.show_practice, fg_color="transparent", 
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w"
        )
        self.practice_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        # Language selection
        self.language_label = ctk.CTkLabel(
            self.sidebar_frame, text="Language:", 
            anchor="w", font=ctk.CTkFont(size=14)
        )
        self.language_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.language_menu = ctk.CTkOptionMenu(
            self.sidebar_frame, values=self.languages,
            variable=self.current_language, command=self.change_language
        )
        self.language_menu.grid(row=6, column=0, padx=20, pady=(10, 10), sticky="ew")
        
        # Appearance mode
        self.appearance_label = ctk.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w", 
            font=ctk.CTkFont(size=14)
        )
        self.appearance_label.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.appearance_menu = ctk.CTkOptionMenu(
            self.sidebar_frame, values=["Light", "Dark", "System"],
            command=self.change_appearance_mode
        )
        self.appearance_menu.grid(row=8, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        # Main content frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Show default page
        self.show_dashboard()
    
    def show_dashboard(self):
        self.clear_main_frame()
        self.current_page = "dashboard"
        self.update_sidebar_buttons()
        
        # Header
        header = ctk.CTkLabel(
            self.main_frame, text=f"Welcome to your {self.current_language.get()} Dashboard", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Content frame
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Progress section
        progress_frame = ctk.CTkFrame(content_frame)
        progress_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        progress_label = ctk.CTkLabel(
            progress_frame, text="Your Progress", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        progress_label.pack(padx=20, pady=(20, 10), anchor="w")
        
        progress_value = self.progress[self.current_language.get()]
        progress_bar = ctk.CTkProgressBar(progress_frame)
        progress_bar.pack(padx=20, pady=10, fill="x")
        progress_bar.set(progress_value / 100)
        
        progress_text = ctk.CTkLabel(
            progress_frame, text=f"{progress_value}% Complete", 
            font=ctk.CTkFont(size=14)
        )
        progress_text.pack(padx=20, pady=(0, 20), anchor="e")
        
        # Stats section
        stats_frame = ctk.CTkFrame(content_frame)
        stats_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        stats_label = ctk.CTkLabel(
            stats_frame, text="Learning Stats", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        stats_label.pack(padx=20, pady=(20, 10), anchor="w")
        
        stats = [
            f"Words Learned: {random.randint(50, 500)}",
            f"Phrases Mastered: {random.randint(10, 100)}",
            f"Daily Streak: {random.randint(1, 30)} days",
            f"Time Spent: {random.randint(5, 50)} hours"
        ]
        
        for stat in stats:
            stat_label = ctk.CTkLabel(stats_frame, text=stat, anchor="w")
            stat_label.pack(padx=20, pady=5, anchor="w", fill="x")
        
        # Recent lessons section
        recent_frame = ctk.CTkFrame(content_frame)
        recent_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        
        recent_label = ctk.CTkLabel(
            recent_frame, text="Continue Learning", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        recent_label.pack(padx=20, pady=(20, 10), anchor="w")
        
        lessons_frame = ctk.CTkFrame(recent_frame, fg_color="transparent")
        lessons_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        lesson_topics = ["Greetings", "Food & Dining", "Travel", "Business"]
        
        for i, topic in enumerate(lesson_topics):
            lesson_button = ctk.CTkButton(
                lessons_frame, text=topic, 
                command=lambda t=topic: self.open_lesson(t)
            )
            lesson_button.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="ew")
            
        lessons_frame.grid_columnconfigure(0, weight=1)
        lessons_frame.grid_columnconfigure(1, weight=1)
    
    def show_lessons(self):
        self.clear_main_frame()
        self.current_page = "lessons"
        self.update_sidebar_buttons()
        
        # Header
        header = ctk.CTkLabel(
            self.main_frame, text=f"{self.current_language.get()} Lessons", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Content frame
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Categories
        categories = ["Beginner", "Intermediate", "Advanced", "Specialized"]
        
        for i, category in enumerate(categories):
            category_frame = ctk.CTkFrame(content_frame)
            category_frame.grid(row=i, column=0, padx=20, pady=10, sticky="ew")
            
            category_label = ctk.CTkLabel(
                category_frame, text=category, 
                font=ctk.CTkFont(size=18, weight="bold")
            )
            category_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
            
            lessons_frame = ctk.CTkFrame(category_frame, fg_color="transparent")
            lessons_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
            
            lesson_topics = [
                f"Lesson {j+1}: {['Basics', 'Conversation', 'Grammar', 'Vocabulary'][j%4]}" 
                for j in range(4)
            ]
            
            for j, topic in enumerate(lesson_topics):
                lesson_button = ctk.CTkButton(
                    lessons_frame, text=topic, 
                    command=lambda t=topic: self.open_lesson(t)
                )
                lesson_button.grid(row=j//2, column=j%2, padx=10, pady=10, sticky="ew")
                
            lessons_frame.grid_columnconfigure(0, weight=1)
            lessons_frame.grid_columnconfigure(1, weight=1)
    
    def show_practice(self):
        self.clear_main_frame()
        self.current_page = "practice"
        self.update_sidebar_buttons()
        
        # Header
        header = ctk.CTkLabel(
            self.main_frame, text="Practice Your Skills", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Content frame
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Practice types
        practice_types_frame = ctk.CTkFrame(content_frame)
        practice_types_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        practice_types = ["Flashcards", "Multiple Choice", "Listening", "Speaking"]
        
        for i, practice_type in enumerate(practice_types):
            practice_button = ctk.CTkButton(
                practice_types_frame, text=practice_type, 
                command=lambda t=practice_type: self.start_practice(t)
            )
            practice_button.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            practice_types_frame.grid_columnconfigure(i, weight=1)
        
        # Sample practice area (flashcards)
        practice_area = ctk.CTkFrame(content_frame)
        practice_area.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        practice_title = ctk.CTkLabel(
            practice_area, text="Flashcards", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        practice_title.pack(padx=20, pady=(20, 10))
        
        flashcard_frame = ctk.CTkFrame(practice_area, height=200)
        flashcard_frame.pack(padx=40, pady=20, fill="x")
        
        word_label = ctk.CTkLabel(
            flashcard_frame, text="Hello", 
            font=ctk.CTkFont(size=24)
        )
        word_label.pack(expand=True, pady=40)
        
        reveal_button = ctk.CTkButton(
            practice_area, text="Reveal Answer", 
            command=lambda: self.reveal_answer(answer_label)
        )
        reveal_button.pack(padx=20, pady=10)
        
        answer_label = ctk.CTkLabel(
            practice_area, text="", 
            font=ctk.CTkFont(size=18)
        )
        answer_label.pack(padx=20, pady=10)
        
        buttons_frame = ctk.CTkFrame(practice_area, fg_color="transparent")
        buttons_frame.pack(padx=20, pady=20, fill="x")
        
        incorrect_button = ctk.CTkButton(
            buttons_frame, text="Incorrect", 
            fg_color="#E74C3C", hover_color="#C0392B",
            command=lambda: self.next_card(word_label, answer_label)
        )
        incorrect_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        correct_button = ctk.CTkButton(
            buttons_frame, text="Correct", 
            fg_color="#2ECC71", hover_color="#27AE60",
            command=lambda: self.next_card(word_label, answer_label)
        )
        correct_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
    
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def update_sidebar_buttons(self):
        buttons = [self.dashboard_button, self.lessons_button, self.practice_button]
        pages = ["dashboard", "lessons", "practice"]
        
        for button, page in zip(buttons, pages):
            if page == self.current_page:
                button.configure(fg_color=("gray75", "gray25"))
            else:
                button.configure(fg_color="transparent")
    
    def change_language(self, new_language):
        self.current_language.set(new_language)
        if self.current_page == "dashboard":
            self.show_dashboard()
        elif self.current_page == "lessons":
            self.show_lessons()
    
    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
    
    def open_lesson(self, lesson_topic):
        self.clear_main_frame()
        
        # Header
        header = ctk.CTkLabel(
            self.main_frame, text=f"Lesson: {lesson_topic}", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Content frame
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        # Lesson content (placeholder)
        lesson_text = """
        This is a sample lesson content. In a real application, this would contain
        the actual lesson material, including text, images, audio, and interactive elements.
        
        The lesson would be structured with clear sections, examples, and practice opportunities.
        """
        
        text_box = ctk.CTkTextbox(content_frame, width=600, height=300)
        text_box.pack(padx=20, pady=20, fill="both", expand=True)
        text_box.insert("1.0", lesson_text)
        text_box.configure(state="disabled")
        
        # Navigation buttons
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(padx=20, pady=(0, 20), fill="x")
        
        back_button = ctk.CTkButton(
            button_frame, text="Back to Lessons", 
            command=self.show_lessons
        )
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        next_button = ctk.CTkButton(
            button_frame, text="Practice this Lesson", 
            command=self.show_practice
        )
        next_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
    
    def start_practice(self, practice_type):
        # This would switch to the selected practice type
        # For this demo, we'll just show a message
        print(f"Starting {practice_type} practice")
    
    def reveal_answer(self, answer_label):
        # In a real app, this would reveal the translation
        answer_label.configure(text="Hola (Spanish)")
    
    def next_card(self, word_label, answer_label):
        # In a real app, this would show the next flashcard
        words = ["Goodbye", "Thank you", "Please", "Yes", "No"]
        word_label.configure(text=random.choice(words))
        answer_label.configure(text="")

if __name__ == "__main__":
    app = LanguageLearningApp()
    app.mainloop()