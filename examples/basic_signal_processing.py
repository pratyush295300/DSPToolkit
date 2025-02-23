import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.generators.signal_generator import SignalGenerator
from src.filters.digital_filters import DigitalFilters
from src.transforms.transforms import SignalTransforms

def main():
    # Parameters
    duration = 1.0  # seconds
    sampling_rate = 1000  # Hz
    signal_freq = 10  # Hz
    noise_amplitude = 0.5
    
    # Generate a clean sine wave
    gen = SignalGenerator()
    t, clean_signal = gen.sine_wave(signal_freq, duration, sampling_rate)
    
    # Add some noise
    _, noise = gen.noise(duration, sampling_rate, noise_amplitude)
    noisy_signal = clean_signal + noise
    
    # Apply a low-pass filter
    filters = DigitalFilters()
    filtered_signal = filters.low_pass_filter(noisy_signal, signal_freq * 2, sampling_rate)
    
    # Compute FFT of the signals
    transforms = SignalTransforms()
    freq_clean, mag_clean, _ = transforms.fft(clean_signal, sampling_rate)
    freq_noisy, mag_noisy, _ = transforms.fft(noisy_signal, sampling_rate)
    freq_filtered, mag_filtered, _ = transforms.fft(filtered_signal, sampling_rate)
    
    # Plotting
    plt.figure(figsize=(15, 10))
    
    # Time domain signals
    plt.subplot(2, 1, 1)
    plt.plot(t, clean_signal, label='Clean')
    plt.plot(t, noisy_signal, label='Noisy')
    plt.plot(t, filtered_signal, label='Filtered')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Time Domain Signals')
    plt.legend()
    plt.grid(True)
    
    # Frequency domain
    plt.subplot(2, 1, 2)
    plt.plot(freq_clean, mag_clean, label='Clean')
    plt.plot(freq_noisy, mag_noisy, label='Noisy')
    plt.plot(freq_filtered, mag_filtered, label='Filtered')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.title('Frequency Domain Signals')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
