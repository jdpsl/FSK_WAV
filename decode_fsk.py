import numpy as np
import wave
from scipy.fft import fft

# Define the parameters
baud_rate = 1200  # bits per second
mark_freq = 1200  # Hz
space_freq = 2200  # Hz
sample_rate = 8000  # samples per second
bit_duration = sample_rate // baud_rate  # samples per bit

# Read the carrier signal from the wav file
wav_file = wave.open("bfsk.wav", "rb")
n_samples = wav_file.getnframes()
carrier = np.frombuffer(wav_file.readframes(n_samples), dtype=np.int16)
wav_file.close()

# Normalize the carrier signal
carrier = carrier / 32767  # scale back to [-1, 1]

# Decode the binary message
bits = ""
for i in range(0, len(carrier), bit_duration):
    segment = carrier[i:i + bit_duration]
    spectrum = np.abs(fft(segment))[:bit_duration // 2]  # perform FFT and take half of the spectrum
    freqs = np.fft.fftfreq(len(segment), d=1/sample_rate)[:bit_duration // 2]

    # Find the dominant frequency in the segment
    dominant_freq = freqs[np.argmax(spectrum)]

    # Determine if it's a mark or space
    if abs(dominant_freq - mark_freq) < abs(dominant_freq - space_freq):
        bits += "0"
    else:
        bits += "1"

# Convert the binary string to the original message
chars = [chr(int(bits[i:i + 8], 2)) for i in range(0, len(bits), 8)]
message = "".join(chars)

print("Decoded message:", message)
