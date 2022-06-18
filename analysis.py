## RUNNING ANALYSIS SCRIPT, COMMENTING AS I GO:
#%% import necessary modules
from random import sample
import numpy as np
from matplotlib import pyplot as plt
from utilities import *

#%% Noise Profiles Sample 7
file_paths_noise = [
    r"sample_7_keysight_edu3321a/20220608_1745_59000_ms.txt",
    r"sample_7_keysight_edu3321a/20220608_1747_60000_ms.txt",
    r"sample_7_keysight_edu3321a/20220610_1607_120000_ms.txt",
    r"sample_7_keysight_edu3321a/20220610_1618_121000_ms.txt",
    r"sample_7_keysight_edu3321a/20220610_1620_122000_ms.txt",
    r"sample_7_keysight_edu3321a/20220610_1624_123000_ms.txt"
]

formatted = False
SR_AD2 = 10000 #Hz
SR_BT = 1500 #Hz
NUM_CHANNELS_BT = 8

#%% Plot noise profiles

# i = 0.3
# for file_path in file_paths_noise:
#     # Load data from files - formats raw bluetooth data files if needed
#     if (formatted):
#         data_BT = np.loadtxt(file_path, comments="#", delimiter=",")
#     else:
#         data = raw_file_to_array(file_path)
#         data_BT = int_to_millivolts(split_data_into_channels(data, NUM_CHANNELS_BT))

#     plot_fft(data_BT, SR_BT, title="Noise FFT, " + file_path, color=str(i))
#     i += 0.1
#     plt.show()
    
# %% Plot raw noise
# color = '0.5'

# formatted = False
# SR_BT = 1500 #Hz
# NUM_CHANNELS_BT = 8

# file_path = r"sample_7_keysight_edu3321a/20220608_1745_59000_ms.txt"
# data_BT = data = raw_file_to_array(file_path)
# data_BT = int_to_millivolts(split_data_into_channels(data, NUM_CHANNELS_BT))
# plot_split_data(data_BT, SR_BT, filtered=False, title="Sample 7 Noise 59", color='C0')
# plt.show()

# file_path = r"sample_7_keysight_edu3321a/20220610_1607_120000_ms.txt"
# data_BT = data = raw_file_to_array(file_path)
# data_BT = int_to_millivolts(split_data_into_channels(data, NUM_CHANNELS_BT))
# plot_split_data(data_BT, SR_BT, filtered=False, title="Sample 7 Noise 120", color='C1')
# plt.show()

# file_path = r"sample_7_keysight_edu3321a/20220610_1624_123000_ms.txt"
# data_BT = data = raw_file_to_array(file_path)
# data_BT = int_to_millivolts(split_data_into_channels(data, NUM_CHANNELS_BT))
# plot_split_data(data_BT, SR_BT, filtered=False, title="Sample 7 Noise 123", color='C2')

# plt.show()
# %% 200 Hz noise removal

# file_path_BT = r"sample_7_keysight_edu3321a/20220608_1843_65000_ms.txt" # 50 Hz

# SR_AD2 = 10000 #Hz
# SR_BT = 1500 #Hz
# NUM_CHANNELS_BT = 8

# data = raw_file_to_array(file_path_BT)
# data_BT = int_to_millivolts(split_data_into_channels(data, NUM_CHANNELS_BT))
# times_BT = np.arange(0, np.size(data_BT[0])) * 1/SR_BT

# #%%
# # Plot windowed FFT of raw data:
# start = 15 * SR_BT
# end = 17 * SR_BT
# plot_fft(data_BT[0:5,start:end], SR_BT, title="Windowed FFT, 275 Hz signal response")
# plt.xlim([0,500])
# plt.show()

# #%%
# # notch filters at 50, 75, 125, 175
# b1, a1 = iir_notch(50, 10, SR_BT)
# b2, a2 = iir_notch(75, 10, SR_BT)
# b3, a3 = butter_bandpass(30,300, SR_BT)

# filtered_data_BT = apply_filter(data_BT, b1, a1)
# filtered_data_BT = apply_filter(filtered_data_BT, b2, a2)
# filtered_data_BT = apply_filter(filtered_data_BT, b3, a3)

# offset = 10.221 + 13.1072 + 0.00115     # seconds
# file_path_AD2 = r"sample_7_keysight_edu3321a/keysight_275Hz_0msOffset"
# wavegen_data = np.loadtxt(file_path_AD2, comments="#", delimiter=",")
# times_wavegen = wavegen_data[:, 0] + offset
# wavegen_data = wavegen_data[:, 1] * 1000    # mV

# # Plot Bluetooth Data with or wo wavegen data

# plot_wavegen = True
# plot_filtered = True

# fig, axs = plt.subplots(4, 1, sharex=True, sharey=True)
# # fig.suptitle('Bluetooth Data')
# fig.set_figwidth(8)
# fig.set_figheight(8)
# plt.xlim([11,11.25])
# for i in np.arange(4):
#     axs[i].set_ylabel("mV, ch" + str(i+1))
#     axs[i].set_xlabel("Time (s)")
#     axs[i].plot(times_BT,data_BT[i])
#     if (plot_wavegen):
#         axs[i].plot(times_wavegen, wavegen_data*0.5)
#     if (plot_filtered):
#         axs[i].plot(times_BT, filtered_data_BT[i])
#     axs[i].legend(["raw output", "wavegen input", "filtered output"])

# # Hide x labels and tick labels for all but bottom plot.
# for ax in axs:
#     ax.label_outer()

# plt.show()
#%% Plot all signals

sample_7_file_paths = [
    # r"sample_7_keysight_edu3321a/20220608_1837_62000_ms.txt",
    # r"sample_7_keysight_edu3321a/20220608_1840_63000_ms.txt",
    # r"sample_7_keysight_edu3321a/20220608_1842_64000_ms.txt",
    # r"sample_7_keysight_edu3321a/20220608_1843_65000_ms.txt"
    r"sample_6_noise/20220220_1229_lbicep_30sec_rest.txt"
]

SR_BT = 1500

i = 3
for file_path in sample_7_file_paths:
    # data = raw_file_to_array(file_path)
    # data_BT = int_to_millivolts(split_data_into_channels(data, NUM_CHANNELS_BT))
    data_BT = np.loadtxt(file_path, comments="#", delimiter=",")
    plot_fft(data_BT, SR_BT, title=file_path + " FFT", color='C' + str(i))
    plt.show()
    i += 1

#%% Can we detect an offset? (answer inconclusive)

# offset_file_paths = [
#     r"sample_7_keysight_edu3321a/20220608_1848_70000_ms.txt",
#     r"sample_7_keysight_edu3321a/20220608_1857_72000_ms.txt"
# ]

# SR_BT = 1500 # Hz

# do_fft = False
# plot_signal = False

# for file_path in offset_file_paths:
#     data = raw_file_to_array(file_path)
#     data_BT = int_to_millivolts(split_data_into_channels(data, NUM_CHANNELS_BT))
#     times_BT = np.arange(0, np.size(data_BT[0])) * 1/SR_BT
#     if do_fft:
#         plot_fft(data_BT,SR_BT, title=file_path + " FFT")
#         plt.show()
#     if plot_split_data:
#         plot_split_data(data_BT, SR_BT, title=file_path)
#     # conclusion: no offset could be detected, channel 2 is not reading signals well?

#%% Sample #5 noise profiles
#%% Noise Profiles Sample 7
# noise_file_path = r"sample_5_AD2_may2022/20220429_1741_163000_ms.txt"

# formatted = False
# SR_AD2 = 10000 #Hz
# SR_BT = 1000 #Hz
# NUM_CHANNELS_BT = 8

# data = raw_file_to_array(noise_file_path)
# data_BT = int_to_millivolts(split_data_into_channels(data, NUM_CHANNELS_BT))

# plot_split_data(data_BT,SR_BT,title="Sample #5 Noise", color='C0')
# plt.show()
# plot_fft(data_BT, SR_BT, title = "Sample #5 Noise FFT", color='C0')
# plt.show()

#%% Frequency Responses Sample #5
# SR_BT = 1000

# signal_file_path = r"sample_5_AD2_may2022/20220429_1741_163000_ms.txt"
# filter = True

# data = raw_file_to_array(signal_file_path)
# data_BT = int_to_millivolts(split_data_into_channels(data, NUM_CHANNELS_BT))
# times_BT = np.arange(0, np.size(data_BT[0])) * 1/SR_BT

# if filter:
#     b1, a1 = iir_notch(58, 8, SR_BT)
#     filtered_data_BT = apply_filter(data_BT, b1, a1)

# offset = 13.1072 # seconds
# file_path_AD2 = r"sample_5_AD2_may2022/test_acq0163.csv"
# wavegen_data = np.loadtxt(file_path_AD2, comments="#", delimiter=",")
# times_wavegen = wavegen_data[:, 0] + offset
# wavegen_data = wavegen_data[:, 1] * 1000    # mV

# plot_wavegen = True
# plot_filtered = True

# fig, axs = plt.subplots(4, 1, sharex=True, sharey=True)
# # fig.suptitle('Bluetooth Data')
# fig.set_figwidth(8)
# fig.set_figheight(8)
# for i in np.arange(4):
#     axs[i].set_ylabel("mV, ch" + str(i+1))
#     axs[i].set_xlabel("Time (s)")
#     axs[i].plot(times_BT,data_BT[i])
#     if (plot_wavegen):
#         axs[i].plot(times_wavegen, wavegen_data)
#     if (plot_filtered):
#         axs[i].plot(times_BT, filtered_data_BT[i])
#     axs[i].legend(["raw output", "wavegen input", "filtered output"])

# plt.show()

#%% colorbar for sweeps?
# from scipy.signal import spectrogram

# sweep_file_paths = [
#     r"sample_7_keysight_edu3321a/20220608_1906_80000_ms.txt",
#     r"sample_7_keysight_edu3321a/20220608_1918_80000_ms.txt",
#     r"sample_7_keysight_edu3321a/20220608_1920_81000_ms.txt",
#     r"sample_7_keysight_edu3321a/20220608_1923_82000_ms.txt"
# ]

# SR_BT = 1500
# #ISSUE ASDF NOT 1D???

# for file_path in sweep_file_paths:
#     data = raw_file_to_array(file_path)
#     data_BT = int_to_millivolts(split_data_into_channels(data, NUM_CHANNELS_BT))
#     times_BT = np.arange(0, np.size(data_BT[0])) * 1/SR_BT
#     asdf = np.transpose(data_BT[1,:])
#     print(np.shape(asdf))
#     f,t,Sxx = spectrogram(asdf, SR_BT, window=100)
#     plt.pcolormesh(t, f, Sxx, shading='gouraud')
#     plt.ylabel('Frequency [Hz]')
#     plt.xlabel('Time [sec]')
#     plt.show()

