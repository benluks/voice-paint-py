"""

rendering/canvas.py
Summary:

Manages the canvas where visual strokes are drawn. It initializes the drawing surface and handles rendering contexts.
Key Classes/Functions:

Canvas: A class responsible for managing the drawing surface.
initialize_canvas(): Sets up the canvas for drawing.
clear_canvas(): Clears the canvas for a new drawing session.
get_canvas(): Returns the current canvas object.
Design Patterns:

Singleton Pattern (potential): Ensures that only one canvas instance exists to manage the drawing context globally.
MVC Pattern (View): Serves as the view component that displays visual output.

"""
import pygame
# from utils.config_loader import ConfigLoader

class Canvas:
    def __init__(self, config_loader):
        self.config_loader = config_loader

        # Load configuration
        self.width = self.config_loader.get('canvas', 'width', 800)
        self.height = self.config_loader.get('canvas', 'height', 600)
        self.background_color = self.config_loader.get('canvas', 'background_color', [255, 255, 255])

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clear_canvas()

    def clear_canvas(self):
        self.screen.fill(self.background_color)
        pygame.display.flip()

    def get_canvas(self):
        return self.screen
