"""

audio/capture.py
Summary:

Manages the audio capture process from the user's microphone, handling real-time audio input and preprocessing tasks.
Key Classes/Functions:

AudioCapture: A class responsible for initializing and managing the microphone input stream.
start_capture(): Starts capturing audio from the microphone.
stop_capture(): Stops capturing audio.
get_audio_stream(): Returns the current audio stream data.
Design Patterns:

Producer-Consumer Pattern: Acts as the producer, capturing audio data to be consumed by the audio analysis module.
Observer Pattern: Notifies observers (like the analysis module) when new audio data is available for processing.

"""
import pyaudio
# from utils.config_loader import ConfigLoader

class AudioCapture:
    def __init__(self, config_loader):
        self.config_loader = config_loader
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = None

        # Load configuration
        self.format = getattr(pyaudio, self.config_loader.get('audio', 'format', 'paInt16'))
        self.channels = self.config_loader.get('audio', 'channels', 1)
        self.rate = self.config_loader.get('audio', 'rate', 44100)
        self.frames_per_buffer = self.config_loader.get('audio', 'frames_per_buffer', 1024)

    def start_capture(self):
        self.stream = self.pyaudio_instance.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.frames_per_buffer
        )

    def stop_capture(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

    def get_audio_stream(self):
        return self.stream.read(self.frames_per_buffer, exception_on_overflow=False)

