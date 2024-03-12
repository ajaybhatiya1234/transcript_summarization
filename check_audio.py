# import numpy as np
# import librosa
# import matplotlib.pyplot as plt

# def plot_waveform(audio_segment, title):
#     plt.figure(figsize=(12, 6))
#     plt.plot(audio_segment.get_array_of_samples())
#     plt.title(title)
#     plt.xlabel('Sample')
#     plt.ylabel('Amplitude')
#     plt.show()


# def calculate_snr(original_audio, adjusted_audio):
#     # Get the array of samples for original and adjusted audio
#     original_samples = np.array(original_audio.get_array_of_samples(), dtype=np.float32)
#     adjusted_samples = np.array(adjusted_audio.get_array_of_samples(), dtype=np.float32)
    
#     # Ensure that the samples have the same length
#     min_length = min(len(original_samples), len(adjusted_samples))
#     original_samples = original_samples[:min_length]
#     adjusted_samples = adjusted_samples[:min_length]
    
#     # Calculate the noise (difference between original and adjusted samples)
#     noise = original_samples - adjusted_samples
    
#     # Calculate SNR in dB
#     snr = 10 * np.log10(np.mean(original_samples**2) / np.mean(noise**2))
    
#     return snr



# def compute_spectral_flatness_measure(audio):
#     # Convert audio samples to float32 arrays
#     y = np.array(audio.get_array_of_samples(), dtype=np.float32)
    
#     # Compute the power spectrum
#     S = np.abs(librosa.stft(y))
    
#     # Compute the geometric mean of the power spectrum and the arithmetic mean of the power spectrum
#     geometric_mean = np.exp(np.mean(np.log(S + 1e-10), axis=0))
#     arithmetic_mean = np.mean(S, axis=0)
    
#     # Compute the Spectral Flatness Measure (SFM)
#     sfm = np.exp(np.mean(np.log(geometric_mean / (arithmetic_mean + 1e-10))))
    
#     return sfm

# # Example usage:
# sfm_orig = compute_spectral_flatness_measure(audio)
# sfm_adj = compute_spectral_flatness_measure(adjusted_audio)

# # Print SFM for both original and adjusted audio segments
# print("Spectral Flatness Measure (SFM) - Original:", sfm_orig)
# print("Spectral Flatness Measure (SFM) - Adjusted:", sfm_adj)