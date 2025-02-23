import numpy as np
from scipy import fft

class SignalTransforms:
    """A class implementing various signal transformations."""
    
    @staticmethod
    def fft(signal_array, sampling_rate):
        """
        Compute the Fast Fourier Transform of a signal.
        
        Args:
            signal_array (numpy.ndarray): Input signal
            sampling_rate (int): Sampling rate in Hz
            
        Returns:
            tuple: (frequencies, magnitudes, phases)
        """
        n = len(signal_array)
        frequencies = fft.fftfreq(n, d=1/sampling_rate)
        spectrum = fft.fft(signal_array)
        magnitudes = np.abs(spectrum)
        phases = np.angle(spectrum)
        
        # Only return positive frequencies
        positive_mask = frequencies >= 0
        return (frequencies[positive_mask], 
                magnitudes[positive_mask],
                phases[positive_mask])
    
    @staticmethod
    def ifft(magnitudes, phases):
        """
        Compute the Inverse Fast Fourier Transform.
        
        Args:
            magnitudes (numpy.ndarray): Magnitude spectrum
            phases (numpy.ndarray): Phase spectrum
            
        Returns:
            numpy.ndarray: Reconstructed time-domain signal
        """
        spectrum = magnitudes * np.exp(1j * phases)
        return np.real(fft.ifft(spectrum))
    
    @staticmethod
    def stft(signal_array, window_size=2048, hop_length=512, window='hann'):
        """
        Compute the Short-Time Fourier Transform.
        
        Args:
            signal_array (numpy.ndarray): Input signal
            window_size (int): Size of the analysis window
            hop_length (int): Number of samples between successive windows
            window (str): Window type ('hann', 'hamming', 'blackman', etc.)
            
        Returns:
            numpy.ndarray: Complex STFT matrix
        """
        if window == 'hann':
            window_func = np.hanning(window_size)
        elif window == 'hamming':
            window_func = np.hamming(window_size)
        elif window == 'blackman':
            window_func = np.blackman(window_size)
        else:
            raise ValueError(f"Unsupported window type: {window}")
            
        return np.array([
            fft.fft(signal_array[i:i+window_size] * window_func)
            for i in range(0, len(signal_array) - window_size, hop_length)
        ])
    
    @staticmethod
    def istft(stft_matrix, window_size=2048, hop_length=512, window='hann'):
        """
        Compute the Inverse Short-Time Fourier Transform.
        
        Args:
            stft_matrix (numpy.ndarray): STFT matrix
            window_size (int): Size of the analysis window
            hop_length (int): Number of samples between successive windows
            window (str): Window type ('hann', 'hamming', 'blackman', etc.)
            
        Returns:
            numpy.ndarray: Reconstructed time-domain signal
        """
        if window == 'hann':
            window_func = np.hanning(window_size)
        elif window == 'hamming':
            window_func = np.hamming(window_size)
        elif window == 'blackman':
            window_func = np.blackman(window_size)
        else:
            raise ValueError(f"Unsupported window type: {window}")
            
        # Initialize output array
        n_frames = len(stft_matrix)
        expected_signal_len = (n_frames - 1) * hop_length + window_size
        reconstructed = np.zeros(expected_signal_len)
        
        # Reconstruct signal
        for i, frame in enumerate(stft_matrix):
            start = i * hop_length
            reconstructed[start:start+window_size] += np.real(fft.ifft(frame)) * window_func
            
        return reconstructed
