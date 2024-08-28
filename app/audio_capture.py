import threading
import pyaudio

CHUNK_SIZE = 128 
RATE = 44100  # Sample rate
FORMAT = pyaudio.paFloat32  # Audio format
CHANNELS = 1  # Number of audio channels

# AudioInputThread class to handle microphone input
class AudioCapture(threading.Thread):
    def __init__(self, audio_queue):
        super().__init__()
        self.audio_queue = audio_queue
        self._stop_event = threading.Event()
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE
        )

    def run(self):
        while not self._stop_event.is_set():
            data = self.stream.read(CHUNK_SIZE, exception_on_overflow=False)
            self.audio_queue.put(data)

    def stop(self):
        self._stop_event.set()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()