import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

# Set the parameters for the audio signal
sampling_rate = 44100  # Sampling rate in Hz
duration = 4.0         # Duration of the audio signal in seconds
frequency = 200.0      # Frequency of the audio signal in Hz (e.g., A4 note)

# Generate time values from 0 to duration with the given sampling rate
t = np.arange(0, duration, 1/sampling_rate)

# Generate the audio signal (in this example, a sine wave)
audio_signal = 0.5 * np.sin(2 * np.pi * frequency * t)

# Scale the audio signal to 16-bit integer range (-32768 to 32767)
scaled_audio_signal = np.int16(audio_signal * 32767)

# Save the audio signal as a WAV file
write('output_audio.wav', sampling_rate, scaled_audio_signal)

# Plot the audio signal
plt.figure(figsize=(10, 4))
plt.plot(t, audio_signal, label='Audio Signal (Sine Wave)')
plt.title('Generated Audio Signal')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.show()
