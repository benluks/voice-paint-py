"""
Acts as the pipeline. All processing workers are deployed from here
"""

import threading
import numpy as np
from PyQt6.QtCore import pyqtSignal, QObject
import analysis

class Processor(QObject):
    analysis_signal = pyqtSignal(dict)  # Signal to emit waveform data

    def __init__(self, audio_queue):
        super().__init__()
        self.audio_queue = audio_queue
        self._stop_event = threading.Event()
        self.frame_size = None # set in the MainWindow class
        self.hop_size = None
        self.sample_rate = None

        # analyzers
        self.mpm = analysis.MPM()


    def start(self):
        self._stop_event.clear()
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):

        buffer = bytearray()
        process_size_bytes = np.dtype(np.float32).itemsize * self.frame_size
        hop_size_bytes = np.dtype(np.float32).itemsize * self.hop_size

        while not self._stop_event.is_set():
            if not self.audio_queue.empty():
                data = self.audio_queue.get()
                buffer.extend(data)
            
                while len(buffer) >= process_size_bytes:
                    process_chunk = buffer[:process_size_bytes]
                    self.process_data(process_chunk)
                    buffer = buffer[process_size_bytes:]

    def stop(self):
        self._stop_event.set()

    def process_data(self, data):
        
        audio_data = np.frombuffer(data, dtype=np.float32).astype(np.float64)
        rms_amplitude = np.sqrt(np.mean(audio_data**2))
        pitch_result = self.mpm.solve(audio_data, self.sample_rate)

        analysis = {
            'audio_data': audio_data,
            'amplitude': rms_amplitude,
            'pitch_result': pitch_result
        }

        self.analysis_signal.emit(analysis)
