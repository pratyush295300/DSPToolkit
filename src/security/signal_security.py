"""
Signal Security Module
Author: Pratyush Padhi
Institution: ITER, SOA University

This module implements security features for signal processing operations.
It provides validation, sanitization, and protection mechanisms for
signal processing applications.
"""

import numpy as np
from typing import Union, Tuple, Optional
import hashlib
import secrets

class SignalSecurity:
    """
    Security utilities for signal processing operations.
    Implements various security checks and validations for signal data.
    """
    
    @staticmethod
    def validate_signal_params(
        frequency: float,
        duration: float,
        sampling_rate: int,
        amplitude: float
    ) -> bool:
        """
        Validate signal parameters to prevent invalid operations.
        
        Args:
            frequency (float): Signal frequency
            duration (float): Signal duration
            sampling_rate (int): Sampling rate
            amplitude (float): Signal amplitude
            
        Returns:
            bool: True if parameters are valid
            
        Raises:
            ValueError: If parameters are invalid
        """
        if not isinstance(frequency, (int, float)) or frequency <= 0:
            raise ValueError("Frequency must be a positive number")
        
        if not isinstance(duration, (int, float)) or duration <= 0:
            raise ValueError("Duration must be a positive number")
            
        if not isinstance(sampling_rate, int) or sampling_rate <= 0:
            raise ValueError("Sampling rate must be a positive integer")
            
        if not isinstance(amplitude, (int, float)):
            raise ValueError("Amplitude must be a number")
            
        # Check Nyquist criterion
        if frequency * 2 >= sampling_rate:
            raise ValueError("Frequency violates Nyquist criterion")
            
        # Check memory constraints
        if duration * sampling_rate > 1e8:  # 100 million samples limit
            raise ValueError("Signal length exceeds memory constraints")
            
        return True
    
    @staticmethod
    def secure_random_noise(
        size: int,
        amplitude: float = 1.0
    ) -> np.ndarray:
        """
        Generate cryptographically secure random noise.
        
        Args:
            size (int): Number of samples
            amplitude (float): Noise amplitude
            
        Returns:
            numpy.ndarray: Secure random noise signal
        """
        # Use secrets module for cryptographic randomness
        random_bytes = secrets.token_bytes(size * 8)  # 8 bytes per float64
        # Convert to array of floats between -1 and 1
        noise = np.frombuffer(random_bytes, dtype='float64')
        noise = (noise / np.max(np.abs(noise))) * amplitude
        return noise[:size]  # Ensure exact size
    
    @staticmethod
    def compute_signal_hash(signal: np.ndarray) -> str:
        """
        Compute cryptographic hash of signal data for integrity verification.
        
        Args:
            signal (numpy.ndarray): Input signal
            
        Returns:
            str: SHA-256 hash of the signal data
        """
        return hashlib.sha256(signal.tobytes()).hexdigest()
    
    @staticmethod
    def validate_array_bounds(
        array: np.ndarray,
        max_size: Optional[int] = None
    ) -> bool:
        """
        Validate array bounds to prevent buffer overflows.
        
        Args:
            array (numpy.ndarray): Input array
            max_size (int, optional): Maximum allowed size
            
        Returns:
            bool: True if array is valid
            
        Raises:
            ValueError: If array bounds are invalid
        """
        if not isinstance(array, np.ndarray):
            raise ValueError("Input must be a numpy array")
            
        if array.size == 0:
            raise ValueError("Array cannot be empty")
            
        if max_size and array.size > max_size:
            raise ValueError(f"Array size exceeds maximum allowed size of {max_size}")
            
        if not np.isfinite(array).all():
            raise ValueError("Array contains non-finite values")
            
        return True
