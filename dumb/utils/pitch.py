import numpy as np
import colorsys
ALPHA = 0.1

def ema(pitch, pitch_prev=None, alpha=ALPHA):

    if not pitch_prev:
        return pitch
    
    return alpha * pitch + (1 - alpha) * pitch_prev


def pitch_to_rgb(f, f_min=80, f_max=400):
    # Step 1: Normalize the logarithm of the frequency
    if f < f_min:
        return (255,255,255)

    log_f = np.log2(f)
    log_f_min = np.log2(f_min)
    log_f_max = np.log2(f_max)
    
    normalized_frequency = (log_f - log_f_min) / (log_f_max - log_f_min)

    hue = normalized_frequency * 360
    
    h = hue / 360.0  # Normalize hue to 0-1 range
    r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
    
    # Step 4: Convert RGB values to 0-255 range
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)

    return r, g, b