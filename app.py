import customtkinter as ctk
from utility.config_manager import load_config, save_config
from UI.dashboard_frame import DashboardFrame
from UI.practice_frame import PracticeFrame
from UI.enunciation_frame import EnunciationFrame  # Add this import

class LanguageLearningApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Set appearance mode from saved config
        self.appearance_mode = load_config()
        ctk.set_appearance_mode(self.appearance_mode)
        
        # Configure window
        self.title("Linguify - Modern Language Learning")
        self.geometry("1100x700")
        self.minsize(800, 600)
        
        # Create variables
        self.current_language = ctk.StringVar(value="Spanish")
        self.current_page = "dashboard"
        self.languages = ["Spanish", "French", "German", "Japanese", "Italian"]
        
        # Initialize frames
        self.dashboard = DashboardFrame(self, self.show_practice, self.current_language)
        self.practice = PracticeFrame(self, self.current_language)
        self.enunciation = EnunciationFrame(self, self.current_language)  # Add this line
        
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._create_sidebar()
        
        # Main content frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Show default page
        self.show_dashboard()
    
    def _create_sidebar(self):
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
        
        self.practice_button = ctk.CTkButton(
            self.sidebar_frame, text="Translation Practice", 
            command=self.show_practice, fg_color="transparent", 
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w"
        )
        self.practice_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Add the Enunciation Practice button
        self.enunciation_button = ctk.CTkButton(
            self.sidebar_frame, text="Enunciation Practice", 
            command=self.show_enunciation, fg_color="transparent", 
            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w"
        )
        self.enunciation_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
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
        # Set the current appearance mode in the menu
        self.appearance_menu.set(self.appearance_mode)
        self.appearance_menu.grid(row=8, column=0, padx=20, pady=(10, 20), sticky="ew")
    
    def show_dashboard(self):
        self.clear_main_frame()
        self.current_page = "dashboard"
        self.update_sidebar_buttons()
        self.dashboard.create_frame(self.main_frame)
    
    def show_practice(self):
        self.clear_main_frame()
        self.current_page = "practice"
        self.update_sidebar_buttons()
        self.practice.create_frame(self.main_frame)
    
    # Add this method for the new page
    def show_enunciation(self):
        self.clear_main_frame()
        self.current_page = "enunciation"
        self.update_sidebar_buttons()
        self.enunciation.create_frame(self.main_frame)
    
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def update_sidebar_buttons(self):
        buttons = [self.dashboard_button, self.practice_button, self.enunciation_button]
        pages = ["dashboard", "practice", "enunciation"]
        
        for button, page in zip(buttons, pages):
            if page == self.current_page:
                button.configure(fg_color=("gray75", "gray25"))
            else:
                button.configure(fg_color="transparent")
    
    def change_language(self, new_language):
        self.current_language.set(new_language)
        if self.current_page == "practice":
            self.show_practice()
        elif self.current_page == "enunciation":
            self.show_enunciation()
    
    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
        # Save the user's preference
        save_config(new_appearance_mode)