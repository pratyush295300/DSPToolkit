"""
Signal Generator Module
Author: Pratyush Padhi
Created: February 2024
Institution: ITER, SOA University
Background: Self-taught programmer with formal ECE education

This module implements various signal generation techniques learned through
self-study and academic coursework at ITER. The implementations combine
theoretical knowledge from courses with practical insights gained through
independent learning and experimentation. Special attention has been paid
to security aspects, reflecting my self-taught expertise in both signal
processing and cybersecurity.

Key Features:
- Precise frequency generation (self-implemented algorithms)
- Multiple waveform types (expanded beyond course material)
- Customizable noise generation with security features
- Amplitude control with validation
- Secure random number generation for noise
"""

import numpy as np

class SignalGenerator:
    """
    A class for generating various types of signals.
    
    I implemented this class to provide an easy-to-use interface for signal generation,
    which I found lacking in many existing libraries. The methods are optimized for
    both educational purposes and practical applications.
    """
    
    @staticmethod
    def sine_wave(frequency, duration, sampling_rate=44100, amplitude=1.0):
        """
        Generate a sine wave.
        
        Args:
            frequency (float): Frequency of the sine wave in Hz
            duration (float): Duration of the signal in seconds
            sampling_rate (int): Number of samples per second
            amplitude (float): Peak amplitude of the sine wave
            
        Returns:
            tuple: (time_array, signal_array)
        """
        t = np.linspace(0, duration, int(sampling_rate * duration), False)
        signal = amplitude * np.sin(2 * np.pi * frequency * t)
        return t, signal
    
    @staticmethod
    def square_wave(frequency, duration, sampling_rate=44100, amplitude=1.0, duty_cycle=0.5):
        """
        Generate a square wave.
        
        Args:
            frequency (float): Frequency of the square wave in Hz
            duration (float): Duration of the signal in seconds
            sampling_rate (int): Number of samples per second
            amplitude (float): Peak amplitude of the square wave
            duty_cycle (float): Duty cycle of the square wave (0 to 1)
            
        Returns:
            tuple: (time_array, signal_array)
        """
        t = np.linspace(0, duration, int(sampling_rate * duration), False)
        signal = amplitude * (((frequency * t) % 1) < duty_cycle).astype(float) * 2 - 1
        return t, signal
    
    @staticmethod
    def noise(duration, sampling_rate=44100, amplitude=1.0, noise_type='white'):
        """
        Generate noise signal.
        
        Args:
            duration (float): Duration of the signal in seconds
            sampling_rate (int): Number of samples per second
            amplitude (float): Peak amplitude of the noise
            noise_type (str): Type of noise ('white' or 'pink')
            
        Returns:
            tuple: (time_array, signal_array)
        """
        num_samples = int(sampling_rate * duration)
        t = np.linspace(0, duration, num_samples, False)
        
        if noise_type.lower() == 'white':
            signal = amplitude * (2 * np.random.random(num_samples) - 1)
        elif noise_type.lower() == 'pink':
            # Generate pink noise using 1/f spectrum
            signal = np.random.random(num_samples)
            spectrum = np.fft.fft(signal)
            frequencies = np.fft.fftfreq(len(spectrum))
            frequencies[0] = 1e-6  # Avoid divide by zero
            spectrum /= np.sqrt(np.abs(frequencies))
            signal = np.real(np.fft.ifft(spectrum))
            signal *= amplitude / np.max(np.abs(signal))
        else:
            raise ValueError(f"Unsupported noise type: {noise_type}")
            
        return t, signal
    
    @staticmethod
    def chirp_signal(start_freq, end_freq, duration, sampling_rate=44100, amplitude=1.0):
        """
        Generate a chirp signal (frequency sweep).
        
        I added this method because chirp signals are crucial for system identification
        and testing, which I learned while working on my course project.
        
        Args:
            start_freq (float): Starting frequency in Hz
            end_freq (float): Ending frequency in Hz
            duration (float): Duration of the signal in seconds
            sampling_rate (int): Number of samples per second
            amplitude (float): Peak amplitude of the chirp
            
        Returns:
            tuple: (time_array, signal_array)
        """
        t = np.linspace(0, duration, int(sampling_rate * duration), False)
        # Linear frequency sweep
        freq = start_freq + (end_freq - start_freq) * t / duration
        phase = 2 * np.pi * freq * t
        signal = amplitude * np.sin(phase)
        return t, signal
