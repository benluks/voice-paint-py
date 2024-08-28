"""

audio/analysis.py
Summary:

Contains audio analysis algorithms to extract amplitude, pitch, and formant information from the captured audio.
Key Classes/Functions:

AudioAnalyzer: A class responsible for processing audio data and extracting key features.
analyze_audio(audio_data): Processes audio data to extract amplitude, pitch, and formants.
get_amplitude(): Returns the current amplitude value.
get_pitch(): Returns the current pitch value.
get_formants(): Returns the current formant values (F1, F2).
Design Patterns:

Observer Pattern: Acts as a subject, notifying observers (like the rendering module) of changes in audio characteristics.
Strategy Pattern (potential): Allows different algorithms for audio analysis (e.g., different pitch detection techniques).

"""
import numpy as np

class AudioAnalyzer:
    def __init__(self, config_loader):
        self.config_loader = config_loader
        self.sample_rate = self.config_loader.get('audio', 'rate', 44100)

    def analyze_audio(self, audio_data):
        amplitude = self.get_amplitude(audio_data)
        pitch = self.get_pitch(audio_data)
        formants = self.get_formants(audio_data)
        return amplitude, pitch, formants

    def get_amplitude(self, audio_data):
        # Calculate the root mean square (RMS) amplitude
        amplitude = np.sqrt(np.mean(np.square(audio_data)))
        return amplitude

    def get_pitch(self, audio_data):
        # Use the autocorrelation method to estimate pitch
        autocorr = np.correlate(audio_data, audio_data, mode='full')
        autocorr = autocorr[len(autocorr) // 2:]
        difference = np.diff(autocorr)
        peak = np.argmax(difference > 0)
        pitch = self.sample_rate / peak if peak else 0
        return pitch

    def get_formants(self, audio_data):
        # Use a basic method to estimate formants (F1, F2)
        # In practice, this might use more sophisticated techniques such as LPC
        from scipy.signal import find_peaks

        # Calculate the FFT and find peaks
        spectrum = np.fft.fft(audio_data)
        freqs = np.fft.fftfreq(len(spectrum))
        peaks, _ = find_peaks(np.abs(spectrum), height=0.1)
        formants = freqs[peaks][:2] * self.sample_rate

        if len(formants) < 2:
            formants = [0, 0]  # Default if less than 2 formants found

        return formants[:2]
