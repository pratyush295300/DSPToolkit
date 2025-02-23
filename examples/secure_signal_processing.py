"""
Secure Signal Processing Example
Author: Pratyush Padhi
Institution: ITER, SOA University

This example demonstrates secure signal processing practices,
combining both DSP concepts and security measures. It shows how
to implement signal processing operations with proper security
controls and validations.
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
from src.security.signal_security import SignalSecurity

def demonstrate_secure_signal_processing():
    # Initialize security module
    security = SignalSecurity()
    
    try:
        # Validate parameters before signal generation
        security.validate_signal_params(
            frequency=1000,  # 1 kHz
            duration=1.0,    # 1 second
            sampling_rate=44100,
            amplitude=0.5
        )
        
        # Generate test signal
        gen = SignalGenerator()
        t, signal = gen.sine_wave(1000, 1.0, 44100, 0.5)
        
        # Compute and store original signal hash
        original_hash = security.compute_signal_hash(signal)
        print(f"Original Signal Hash: {original_hash}")
        
        # Generate secure random noise
        noise = security.secure_random_noise(len(signal), 0.1)
        
        # Add noise to signal
        noisy_signal = signal + noise
        
        # Validate array bounds before filtering
        security.validate_array_bounds(noisy_signal)
        
        # Apply filtering
        filters = DigitalFilters()
        filtered_signal = filters.low_pass_filter(
            noisy_signal,
            cutoff_freq=1500,
            sampling_rate=44100
        )
        
        # Verify signal integrity after filtering
        filtered_hash = security.compute_signal_hash(filtered_signal)
        print(f"Filtered Signal Hash: {filtered_hash}")
        
        # Plot results with security information
        plt.figure(figsize=(15, 10))
        
        plt.subplot(3, 1, 1)
        plt.plot(t, signal)
        plt.title(f'Original Signal (Hash: {original_hash[:8]}...)')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.grid(True)
        
        plt.subplot(3, 1, 2)
        plt.plot(t, noisy_signal)
        plt.title('Signal + Secure Random Noise')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.grid(True)
        
        plt.subplot(3, 1, 3)
        plt.plot(t, filtered_signal)
        plt.title(f'Filtered Signal (Hash: {filtered_hash[:8]}...)')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()
        
    except ValueError as e:
        print(f"Security Validation Error: {e}")
    except Exception as e:
        print(f"Processing Error: {e}")

if __name__ == "__main__":
    demonstrate_secure_signal_processing()
