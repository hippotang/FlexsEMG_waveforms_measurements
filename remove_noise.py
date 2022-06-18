# %%
## removing noise from a FlexsEMG given noise profile:
import numpy as np
from matplotlib import pyplot as plt
from utilities import *

# choose files for noise and signal
noise_filepath = r"sample_7_keysight_edu3321a/20220610_1618_121000_ms.txt"
signal_filepath = r"sample_7_keysight_edu3321a/20220608_1835_61000_ms.txt"

# Load data from files - formats raw bluetooth data files if needed
using_unformatted_bluetooth_data_file = True

SAMPLE_RATE = 1500 #Hz
NUM_CHANNELS_BT = 8

if (not using_unformatted_bluetooth_data_file):
    noise_data = np.loadtxt(noise_filepath, comments="#", delimiter=",")
    signal_data = np.loadtxt(signal_filepath, comments="#", delimiter=",")
else:
    noise_data = raw_file_to_array(noise_filepath)
    noise_data = int_to_millivolts(split_data_into_channels(noise_data, NUM_CHANNELS_BT))
    signal_data = raw_file_to_array(signal_filepath)
    signal_data = int_to_millivolts(split_data_into_channels(signal_data, NUM_CHANNELS_BT))

signal_times = np.arange(0, np.size(signal_data[0])) * 1/SAMPLE_RATE

# get FFT for both signals
noise_freqs, noise_fft = get_fft(noise_data, SAMPLE_RATE)
noise_fft_abs = np.abs(noise_fft)
signal_freqs, signal_fft = get_fft(signal_data, SAMPLE_RATE)
new_signal_fft = np.copy(signal_fft)

channel_idx = 3     # (channel number - 1)

noise_max_val = np.amax(noise_fft_abs, axis=1)[channel_idx]
new_signal_fft[channel_idx] *= (-1*np.interp(signal_freqs, noise_freqs, noise_fft_abs[channel_idx], left=0, right=0) + noise_max_val)/noise_max_val


# %%
# Filter based on noise
new_signal_data = np.fft.ifft(new_signal_fft[channel_idx]) * SAMPLE_RATE

plt.figure()
plt.plot(signal_times, signal_data[channel_idx])
plt.plot(signal_times, new_signal_data)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (mV)")

plt.show()
# %%
plt.figure()
plt.plot(noise_freqs, noise_fft_abs[channel_idx])
plt.plot(signal_freqs, np.abs(new_signal_fft[channel_idx]))


plt.show()

# %%
