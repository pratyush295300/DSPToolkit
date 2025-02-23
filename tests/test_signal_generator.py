import sys
import os
import numpy as np
import pytest

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.generators.signal_generator import SignalGenerator

def test_sine_wave_generation():
    """Test sine wave generator."""
    gen = SignalGenerator()
    frequency = 10  # Hz
    duration = 1.0  # second
    sampling_rate = 1000  # Hz
    amplitude = 2.0
    
    t, signal = gen.sine_wave(frequency, duration, sampling_rate, amplitude)
    
    # Check basic properties
    assert len(t) == len(signal)
    assert len(t) == int(duration * sampling_rate)
    assert np.abs(signal).max() == pytest.approx(amplitude, rel=1e-5)
    
    # Check frequency
    fft = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(t), 1/sampling_rate)
    main_freq = freqs[np.argmax(np.abs(fft))]
    assert abs(abs(main_freq) - frequency) < 1.0

def test_square_wave_generation():
    """Test square wave generator."""
    gen = SignalGenerator()
    frequency = 10  # Hz
    duration = 1.0  # second
    sampling_rate = 1000  # Hz
    amplitude = 2.0
    
    t, signal = gen.square_wave(frequency, duration, sampling_rate, amplitude)
    
    # Check basic properties
    assert len(t) == len(signal)
    assert len(t) == int(duration * sampling_rate)
    assert np.abs(signal).max() == pytest.approx(amplitude, rel=1e-5)

def test_noise_generation():
    """Test noise generator."""
    gen = SignalGenerator()
    duration = 1.0  # second
    sampling_rate = 1000  # Hz
    amplitude = 2.0
    
    # Test white noise
    t, white_noise = gen.noise(duration, sampling_rate, amplitude, 'white')
    assert len(t) == len(white_noise)
    assert len(t) == int(duration * sampling_rate)
    assert np.abs(white_noise).max() <= amplitude
    
    # Test pink noise
    t, pink_noise = gen.noise(duration, sampling_rate, amplitude, 'pink')
    assert len(t) == len(pink_noise)
    assert len(t) == int(duration * sampling_rate)
    assert np.abs(pink_noise).max() <= amplitude
    
    # Test invalid noise type
    with pytest.raises(ValueError):
        gen.noise(duration, sampling_rate, amplitude, 'invalid_type')
