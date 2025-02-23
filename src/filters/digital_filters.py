import numpy as np
from scipy import signal

class DigitalFilters:
    """A class implementing various digital filters."""
    
    @staticmethod
    def low_pass_filter(signal_array, cutoff_freq, sampling_rate, order=4):
        """
        Apply a low-pass Butterworth filter to the signal.
        
        Args:
            signal_array (numpy.ndarray): Input signal
            cutoff_freq (float): Cutoff frequency in Hz
            sampling_rate (int): Sampling rate in Hz
            order (int): Filter order
            
        Returns:
            numpy.ndarray: Filtered signal
        """
        nyquist = sampling_rate / 2
        normalized_cutoff = cutoff_freq / nyquist
        b, a = signal.butter(order, normalized_cutoff, btype='low')
        return signal.filtfilt(b, a, signal_array)
    
    @staticmethod
    def high_pass_filter(signal_array, cutoff_freq, sampling_rate, order=4):
        """
        Apply a high-pass Butterworth filter to the signal.
        
        Args:
            signal_array (numpy.ndarray): Input signal
            cutoff_freq (float): Cutoff frequency in Hz
            sampling_rate (int): Sampling rate in Hz
            order (int): Filter order
            
        Returns:
            numpy.ndarray: Filtered signal
        """
        nyquist = sampling_rate / 2
        normalized_cutoff = cutoff_freq / nyquist
        b, a = signal.butter(order, normalized_cutoff, btype='high')
        return signal.filtfilt(b, a, signal_array)
    
    @staticmethod
    def band_pass_filter(signal_array, low_cutoff, high_cutoff, sampling_rate, order=4):
        """
        Apply a band-pass Butterworth filter to the signal.
        
        Args:
            signal_array (numpy.ndarray): Input signal
            low_cutoff (float): Lower cutoff frequency in Hz
            high_cutoff (float): Upper cutoff frequency in Hz
            sampling_rate (int): Sampling rate in Hz
            order (int): Filter order
            
        Returns:
            numpy.ndarray: Filtered signal
        """
        nyquist = sampling_rate / 2
        normalized_cutoffs = [low_cutoff / nyquist, high_cutoff / nyquist]
        b, a = signal.butter(order, normalized_cutoffs, btype='band')
        return signal.filtfilt(b, a, signal_array)
    
    @staticmethod
    def moving_average(signal_array, window_size):
        """
        Apply a simple moving average filter.
        
        Args:
            signal_array (numpy.ndarray): Input signal
            window_size (int): Size of the moving average window
            
        Returns:
            numpy.ndarray: Filtered signal
        """
        window = np.ones(window_size) / window_size
        return np.convolve(signal_array, window, mode='same')
