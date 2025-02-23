import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.generators.signal_generator import SignalGenerator
from src.filters.digital_filters import DigitalFilters
from src.transforms.transforms import SignalTransforms

def spectral_noise_reduction(signal, noise_floor_percentile=30, reduction_factor=0.7):
    """
    Reduce noise using spectral subtraction method.
    
    Args:
        signal: Input signal array
        noise_floor_percentile: Percentile to estimate noise floor
        reduction_factor: Amount of noise reduction (0 to 1)
    
    Returns:
        Cleaned signal array
    """
    # Compute STFT
    transforms = SignalTransforms()
    stft_matrix = transforms.stft(signal)
    
    # Estimate noise floor from magnitude spectrum
    magnitudes = np.abs(stft_matrix)
    noise_floor = np.percentile(magnitudes, noise_floor_percentile, axis=1)
    
    # Apply spectral subtraction
    noise_reduced = np.maximum(
        magnitudes - noise_floor[:, np.newaxis] * reduction_factor,
        magnitudes * 0.1  # Keep at least 10% of original magnitude
    )
    
    # Reconstruct signal with original phase
    phases = np.angle(stft_matrix)
    stft_cleaned = noise_reduced * np.exp(1j * phases)
    
    # Inverse STFT
    return transforms.istft(stft_cleaned)

def main():
    # Parameters
    duration = 3.0  # seconds
    sampling_rate = 8000  # Hz
    
    # Generate a complex test signal (mixture of frequencies)
    gen = SignalGenerator()
    t, signal1 = gen.sine_wave(frequency=400, duration=duration, 
                              sampling_rate=sampling_rate, amplitude=0.5)
    _, signal2 = gen.sine_wave(frequency=800, duration=duration, 
                              sampling_rate=sampling_rate, amplitude=0.3)
    clean_signal = signal1 + signal2
    
    # Add significant noise
    _, noise = gen.noise(duration=duration, sampling_rate=sampling_rate, 
                        amplitude=0.4, noise_type='white')
    noisy_signal = clean_signal + noise
    
    # Apply two different noise reduction methods
    
    # Method 1: Simple low-pass filtering
    filters = DigitalFilters()
    filtered_signal = filters.low_pass_filter(noisy_signal, 
                                            cutoff_freq=1000, 
                                            sampling_rate=sampling_rate)
    
    # Method 2: Spectral noise reduction
    spectral_cleaned = spectral_noise_reduction(noisy_signal)
    
    # Plot results
    plt.figure(figsize=(15, 10))
    
    # Time domain plots
    plt.subplot(3, 2, 1)
    plt.plot(t, clean_signal)
    plt.title('Original Clean Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    plt.subplot(3, 2, 2)
    plt.plot(t, noisy_signal)
    plt.title('Noisy Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    plt.subplot(3, 2, 3)
    plt.plot(t, filtered_signal)
    plt.title('Low-pass Filtered Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    plt.subplot(3, 2, 4)
    plt.plot(t, spectral_cleaned)
    plt.title('Spectral Noise Reduction')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    # Frequency domain plots
    transforms = SignalTransforms()
    
    # Plot original signal spectrum
    freq_clean, mag_clean, _ = transforms.fft(clean_signal, sampling_rate)
    plt.subplot(3, 2, 5)
    plt.plot(freq_clean, mag_clean)
    plt.title('Frequency Spectrum - Clean Signal')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.grid(True)
    
    # Plot noise-reduced signal spectrum
    freq_reduced, mag_reduced, _ = transforms.fft(spectral_cleaned, sampling_rate)
    plt.subplot(3, 2, 6)
    plt.plot(freq_reduced, mag_reduced)
    plt.title('Frequency Spectrum - Noise Reduced')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
