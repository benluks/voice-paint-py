# test_analysis.py
import numpy as np
import analysis

# Create an instance of MPM
mpm = analysis.MPM()

# Generate a test signal (e.g., a sine wave)
sample_rate = 44100
duration = 0.01  # 1 second
frequency = 440.0  # A4 note

t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
signal = 0.5 * np.sin(2 * np.pi * frequency * t)

# Use the solve method to detect the pitch
result = mpm.solve(signal, sample_rate)

print(f"Detected pitch: {result.pitch} Hz")
print(f"Is voiced: {result.voiced}")
