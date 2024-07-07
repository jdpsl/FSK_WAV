import numpy as np
import wave

# Define the parameters
baud_rate = 1200  # bits per second
mark_freq = 1200  # Hz
space_freq = 2200  # Hz
sample_rate = 8000  # samples per second
bit_duration = sample_rate // baud_rate  # samples per bit
message = "Hello World"  # the message to encode
bits = "".join(format(ord(c), "08b") for c in message)  # the message in binary

# Generate the carrier signal
carrier = np.array([])
for bit in bits:
    if bit == "0":
        freq = mark_freq
    else:
        freq = space_freq
    t = np.arange(bit_duration) / sample_rate  # time axis
    tone = np.sin(2 * np.pi * freq * t)  # sinusoidal tone
    carrier = np.append(carrier, tone)  # append tone to carrier

# Normalize the carrier signal
carrier = carrier / np.max(np.abs(carrier))  # scale to [-1, 1]
carrier = (carrier * 32767).astype(np.int16)  # convert to 16-bit PCM

# Write the carrier signal to a wav file
wav_file = wave.open("bfsk.wav", "wb")
wav_file.setparams((1, 2, sample_rate, 0, "NONE", "NONE"))  # set the parameters
wav_file.writeframes(carrier)  # write the frames
wav_file.close()  # close the file




print("Wrote File")
