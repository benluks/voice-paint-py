"""

Root Directory
main.py
Summary:

The entry point of the application. It initializes and orchestrates the components of the application, setting up the event loop and starting the main processes.
Key Classes/Functions:

main(): The main function that initializes the application components and starts the application loop.
setup_app(): A helper function to initialize and configure the components (UI, audio capture, analysis, rendering, etc.).
Design Patterns:

Mediator Pattern: The main function may act as a simple coordinator or use the Mediator to initialize modules and manage interactions between them.
Facade Pattern: Provides a unified interface for initializing and starting the application, hiding complex subsystem interactions.

"""
from audio.capture import AudioCapture
from rendering.canvas import Canvas
from ui.interface import UserInterface
from utils.config_loader import ConfigLoader

def start_audio_capture():
    audio_capture.start_capture()
    print("Audio capture started.")

def stop_audio_capture():
    audio_capture.stop_capture()
    print("Audio capture stopped.")

if __name__ == "__main__":
    # Initialize configuration loader
    config_loader = ConfigLoader()

    # Pass the config loader to each component
    audio_capture = AudioCapture(config_loader)
    canvas = Canvas(config_loader)
    ui = UserInterface(start_audio_capture, stop_audio_capture, config_loader)

    ui.run()
