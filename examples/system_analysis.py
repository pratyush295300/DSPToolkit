"""
System Analysis Example
Author: Pratyush Padhi
Institution: ITER, SOA University

This example demonstrates system analysis using chirp signals,
a technique I learned in my Signal Processing course at ITER.
As someone interested in both DSP and cybersecurity, I've included
considerations for secure signal processing applications.

It shows how to:
1. Generate a chirp signal
2. Apply it to a system (filter)
3. Analyze the system's frequency response
4. Implement secure signal processing practices
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.generators.signal_generator import SignalGenerator
from src.filters.digital_filters import DigitalFilters
from src.transforms.transforms import SignalTransforms

def analyze_system_response():
    # Parameters
    duration = 2.0  # seconds
    sampling_rate = 44100  # Hz
    start_freq = 20  # Hz
    end_freq = 20000  # Hz
    
    # Generate chirp signal
    gen = SignalGenerator()
    t, chirp = gen.chirp_signal(start_freq, end_freq, duration, sampling_rate)
    
    # Create a system to analyze (bandpass filter)
    filters = DigitalFilters()
    filtered_chirp = filters.band_pass_filter(
        chirp, 
        low_cutoff=1000,  # 1kHz
        high_cutoff=5000,  # 5kHz
        sampling_rate=sampling_rate
    )
    
    # Compute frequency response
    transforms = SignalTransforms()
    freq_in, mag_in, _ = transforms.fft(chirp, sampling_rate)
    freq_out, mag_out, _ = transforms.fft(filtered_chirp, sampling_rate)
    
    # Calculate system response
    system_response = mag_out / np.where(mag_in > 1e-10, mag_in, 1e-10)
    
    # Plotting
    plt.figure(figsize=(15, 10))
    
    # Time domain signals
    plt.subplot(3, 1, 1)
    plt.plot(t, chirp, label='Input Chirp')
    plt.plot(t, filtered_chirp, label='Filtered Output')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Time Domain Analysis')
    plt.legend()
    plt.grid(True)
    
    # Input and output spectra
    plt.subplot(3, 1, 2)
    plt.semilogx(freq_in, 20 * np.log10(mag_in + 1e-10), label='Input Spectrum')
    plt.semilogx(freq_out, 20 * np.log10(mag_out + 1e-10), label='Output Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.title('Frequency Domain Analysis')
    plt.legend()
    plt.grid(True)
    
    # System frequency response
    plt.subplot(3, 1, 3)
    plt.semilogx(freq_in, 20 * np.log10(system_response))
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.title('System Frequency Response')
    plt.axvline(1000, color='r', linestyle='--', label='Lower cutoff')
    plt.axvline(5000, color='r', linestyle='--', label='Upper cutoff')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    analyze_system_response()
