"""

ui/interface.py
Summary:

Manages the main user interface layout and elements, providing controls and displays for user interactions.
Key Classes/Functions:

UserInterface: A class responsible for initializing and managing the user interface.
setup_ui(): Sets up the main interface layout and elements.
update_ui(): Updates UI elements based on application state.
display_canvas(canvas): Embeds the rendering canvas within the UI.
Design Patterns:

MVC Pattern (View): Serves as the view component, managing the presentation layer and user interactions.

"""
import pygame
from utils.config_loader import ConfigLoader

class UserInterface:
    def __init__(self, start_callback, stop_callback, config_loader):
        # Load configuration
        self.config_loader = config_loader
        self.window_title = self.config_loader.get('ui', 'window_title', 'Voice Paint')
        self.width = self.config_loader.get('canvas', 'width', 800)
        self.height = self.config_loader.get('canvas', 'height', 600)

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.window_title)

        # Define button properties
        self.button_font = pygame.font.SysFont(None, 36)
        self.start_button = pygame.Rect(50, self.height - 80, 100, 50)  # Position and size
        self.stop_button = pygame.Rect(200, self.height - 80, 100, 50)

        # Callbacks for button actions
        self.start_callback = start_callback
        self.stop_callback = stop_callback

        # Run the main loop
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.draw_ui()
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.start_button.collidepoint(event.pos):
                        self.start_callback()
                    elif self.stop_button.collidepoint(event.pos):
                        self.stop_callback()

    def draw_ui(self):
        # Clear screen with a background color
        self.screen.fill(self.config_loader.get('canvas', 'background_color', (255, 255, 255)))

        # Draw Start button
        pygame.draw.rect(self.screen, (0, 128, 0), self.start_button)
        start_text = self.button_font.render('Start', True, (255, 255, 255))
        self.screen.blit(start_text, (self.start_button.x + 10, self.start_button.y + 10))

        # Draw Stop button
        pygame.draw.rect(self.screen, (128, 0, 0), self.stop_button)
        stop_text = self.button_font.render('Stop', True, (255, 255, 255))
        self.screen.blit(stop_text, (self.stop_button.x + 10, self.stop_button.y + 10))
