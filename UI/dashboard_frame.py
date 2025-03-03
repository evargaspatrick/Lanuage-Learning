import customtkinter as ctk

class DashboardFrame:
    def __init__(self, parent, show_practice_callback, current_language):
        self.parent = parent
        self.show_practice = show_practice_callback
        self.current_language = current_language
        
    def create_frame(self, container):
        # Header
        header = ctk.CTkLabel(
            container, text=f"Welcome to Linguify", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Content frame
        content_frame = ctk.CTkFrame(container)
        content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Welcome message
        welcome_label = ctk.CTkLabel(
            content_frame, 
            text="Start practicing your language skills with our translation tool.",
            font=ctk.CTkFont(size=16)
        )
        welcome_label.pack(padx=20, pady=30)
        
        # Practice button
        practice_button = ctk.CTkButton(
            content_frame, text="Begin Translation Practice",
            command=self.show_practice,
            height=50, font=ctk.CTkFont(size=16)
        )
        practice_button.pack(padx=20, pady=20)
        
        # Selected language info
        language_info = ctk.CTkLabel(
            content_frame,
            text=f"Currently selected language: {self.current_language.get()}",
            font=ctk.CTkFont(size=14)
        )
        language_info.pack(padx=20, pady=20)