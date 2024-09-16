# test_analysis.py
import numpy as np
import analysis

# Create an instance of MPM
formant_processor = analysis.Formants()

# Generate a test signal (e.g., a sine wave)
sample_rate = 44100
duration = 0.05  # 5 seconds
frequency = 440.0  # A4 note

t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
signal = np.random.randn((int(duration * sample_rate),))

# Use the solve method to detect the pitch
result = formant_processor.processData(signal, sample_rate)

print(f"Detected pitch: {result.pitch} Hz")
print(f"Is voiced: {result.voiced}")
