import customtkinter as ctk
from app import LanguageLearningApp
from utility.config_manager import load_config
import pygame  # Add this import

if __name__ == "__main__":
    # Initialize pygame mixer at startup
    try:
        pygame.mixer.init()
        print("Pygame mixer initialized successfully")
    except Exception as e:
        print(f"Warning: Could not initialize pygame mixer: {e}")
    
    # Set appearance mode from saved config
    appearance_mode = load_config()
    ctk.set_appearance_mode(appearance_mode)
    
    # Set default color theme
    ctk.set_default_color_theme("blue")
    
    # Launch application
    app = LanguageLearningApp()
    app.mainloop()
    
    # Clean up pygame resources on exit
    try:
        pygame.mixer.quit()
        pygame.quit()
    except:
        pass