# %%
# import necessary modules
import wave
import numpy as np
from matplotlib import pyplot as plt
from utilities import *

# %%
# CHANGE AS NEEDED: specify the bluetooth data file 
color = '0.5'
file_path_BT = r"sample_7_keysight_edu3321a/20220608_1835_61000_ms.txt" # 50 Hz
file_path_BT = r"sample_7_keysight_edu3321a/20220610_1618_121000_ms.txt" # noise
# file_path_BT = r"sample_7_keysight_edu3321a/20220610_1620_122000_ms.txt" # noise

# CHANGE AS NEEDED: is the above file unformatted?
using_unformatted_bluetooth_data_file = True

# these are constants, do NOT change them
SR_AD2 = 10000 #Hz
SR_BT = 1500 #Hz
NUM_CHANNELS_BT = 8

# Load data from files - formats raw bluetooth data files if needed
if (not using_unformatted_bluetooth_data_file):
    data_BT = np.loadtxt(file_path_BT, comments="#", delimiter=",")
else:
    data = raw_file_to_array(file_path_BT)
    data_BT = int_to_millivolts(split_data_into_channels(data, NUM_CHANNELS_BT))

# print shapes of data
print("shape of BT data: " + str(np.shape(data_BT)))

# convenient variables to reference data
times_BT = np.arange(0, np.size(data_BT[0])) * 1/SR_BT

# %% 
# Filter
# b, a = iir_notch(60.2, 10, SR_BT)
# b, a = butter_bandstop(59, 61, SR_BT)
# data_BT = apply_filter(data_BT, b, a)

# # Generate sin wave
using_wavegen_file = True

if not using_wavegen_file:
    times_wavegen = np.copy(times_BT)
    FREQ = 50   # Hz
    wavegen_data = np.sin(2*np.pi*FREQ * times_wavegen)
else:
    offset = 10.221 - (-13.1072)     # seconds
    file_path_AD2 = r"sample_7_keysight_edu3321a/keysight_50Hz_0msOffset"
    wavegen_data = np.loadtxt(file_path_AD2, comments="#", delimiter=",")
    times_wavegen = wavegen_data[:, 0] + offset
    wavegen_data = wavegen_data[:, 1] * 1000    # mV
# %%
# Plot Bluetooth Data with or wo wavegen data

plot_wavegen = False

fig, axs = plt.subplots(5, 1, sharex=True, sharey=True)
fig.suptitle('Bluetooth Data')
fig.set_figwidth(16)
fig.set_figheight(NUM_CHANNELS_BT*2)
for i in np.arange(5):
    axs[i].set_ylabel("mV, ch" + str(i+1))
    axs[i].set_xlabel("Time (s)")
    axs[i].plot(times_BT,data_BT[i])
    if (plot_wavegen):
        axs[i].plot(times_wavegen, wavegen_data)

# Hide x labels and tick labels for all but bottom plot.
for ax in axs:
    ax.label_outer()

# Plot FFT
fft_title = file_path_BT + " FFT Magnitude"
plot_fft(data_BT[0:5,1500*12:], SR_BT, title=fft_title, color=color)
plt.show()

# # Plot only the first channel
# f2 = plt.plot(times_BT, data_BT[0])
# plt.ylabel("mV, ch1")
# plt.xlabel("Time (s)")
# plt.show()