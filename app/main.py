import sys
import numpy as np
import queue
from audio_capture import AudioCapture
from processor import Processor
from config_loader import ConfigLoader
from utils.pitch import ema, pitch_to_rgb

from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt6.QtCore import QLineF
from PyQt6.QtGui import QPainter, QColor, QPen


loader = ConfigLoader()
loader.load_config()

sample_rate = loader.get('audio', 'rate')
# process_frame = loader.get('processor', 'process_frame_ms')
window_length = 50 # ms
hop_length = window_length // 2

processing_chunk_size = int(window_length / 1000 * sample_rate)  # Size of chunks to process
processing_window_slide = int(hop_length / 1000 * sample_rate)

# MainWindow class for the PyQt application
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Waveform Display")
        self.setGeometry(100, 100, 600, 400)

        self.capture_thread = AudioCapture(audio_queue=None)
        self.processing_thread = Processor(audio_queue=None)

        self.processing_thread.analysis_signal.connect(self.update_analysis)

        # Create UI elements
        layout = QVBoxLayout(self)

        # Create a widget for the waveform display
        self.waveform_display = QWidget(self)
        layout.addWidget(self.waveform_display)

        # Set up buttons at the bottom
        button_layout = QHBoxLayout()
        self.start_button = QPushButton(text="Start", parent=self)
        self.stop_button = QPushButton("Stop", self)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        # Add button layout to the main layout
        layout.addLayout(button_layout)


        # Connect buttons to functions
        self.start_button.clicked.connect(self.start_audio_processing)
        self.stop_button.clicked.connect(self.stop_audio_processing)

        # Set up waveform data
        self.waveform_data = np.zeros(processing_chunk_size)
        self.pitch_track = [0.]
        self.amplitdue_track = [0.]

    def start_audio_processing(self):
        self.audio_queue = queue.Queue()

        self.capture_thread.audio_queue = self.audio_queue
        self.processing_thread.audio_queue = self.audio_queue

        self.processing_thread.frame_size = processing_chunk_size
        self.processing_thread.hop_size = processing_window_slide
        self.processing_thread.sample_rate = sample_rate
        
        self.capture_thread.start()
        self.processing_thread.start()

    def stop_audio_processing(self):
        self.capture_thread.stop()
        self.processing_thread.stop()

    def update_analysis(self, analysis):
        self.waveform_data = analysis['audio_data']
        
        amplitude = analysis['amplitude']
        pitch_result = analysis['pitch_result']
        

        if pitch_result.voiced:
            smoothed_pitch = ema(pitch_result.pitch, self.pitch_track[-1])
            smoothed_amplitude = ema(amplitude, self.amplitdue_track[-1])
        else:
            smoothed_pitch = pitch_result.pitch
            smoothed_amplitude = amplitude
        
        print(smoothed_amplitude)
        self.pitch_track.append(smoothed_pitch)
        self.amplitdue_track.append(smoothed_amplitude)

        self.update()


    def paintEvent(self, event):
        # Paint the waveform on the window
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Clear the window
        painter.fillRect(self.rect(), QColor("black"))

        # Set pen for waveform
        pen = QPen(QColor(*pitch_to_rgb(self.pitch_track[-1])))
        pen.setWidth(round(self.amplitdue_track[-1]*100))
        painter.setPen(pen)

        # Calculate the center and scale of the waveform
        center_y = self.height() / 2
        
        scale_x = self.width() / processing_chunk_size
        scale_y = center_y * 0.8
        
        xs = np.rint(np.arange(self.waveform_data.size) * scale_x)
        ys = np.rint(center_y - self.waveform_data * scale_y)
        
        # Draw the waveform
        for i in range(1, len(xs)):
            
            painter.drawLine(QLineF(xs[i-1], ys[i-1], xs[i], ys[i]))


# Main function to run the application
def main():
    app = QApplication(sys.argv)

      # Will be set in MainWindow
    
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
