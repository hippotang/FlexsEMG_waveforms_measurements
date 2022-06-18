## utility functions
## if argument is split_data, then each row contains data for one channel
## if argument is channel_data, then it is a 1d array of data for 1 channel

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft
import sys

def hex_string_to_int(hex_string):
    hex_str = "0x" + str(hex_string)
    return np.int16(int(hex_str, 16))

# data can be any shape, just does scalar multiplication
# found on page 8 of intan RHD2000 datasheet
def int_to_millivolts(data, invert_voltage=False):
    multiplier = 0.195E-3
    if (invert_voltage):
        multiplier *= -1
    return data * multiplier

# If your raw data file contains one BLE packet per new line, 
# then use this function to format it into a 1d array
def raw_file_to_array(file_path):
    emg = []
    # open file
    file = open(file_path, "r")
    # read first line
    line = file.readline()
    # while the line is not empty, get the data
    # and append it to emg 
    while line:
        data = line.strip()
        data = data.split()
        if len(data) >= 240:
            for i in range(0,239,2):
                emg.append(hex_string_to_int(
                    data[i+1] + data[i]
                ))
        line = file.readline()

    file.close()
    return np.array(emg)

# use this function after raw_file_to_array
# to split the returned array into num_channels
def split_data_into_channels(emg_integer_array, num_channels):
    total_data_pts = np.size(emg_integer_array)
    offset = total_data_pts % num_channels
    num_cols = int(total_data_pts / num_channels)
    if (offset != 0):
        emg_integer_array = emg_integer_array[0:-offset]

    print("num_cols: " + str(num_cols))

    split_data = np.reshape(emg_integer_array, (num_channels, num_cols), order='F')
    return split_data

# saves split data in a csv format
def save_split_data_as_csv(split_data, new_file_name, num_channels, sample_rate):
    file_path = new_file_name
    length = np.shape(split_data)[1] / sample_rate
    header_txt = "{}: {}-channel, {}Hz, length: {}seconds, values in millivolts".format(
        new_file_name, num_channels, sample_rate, length)
    np.savetxt(file_path, split_data, fmt="%1.3e", delimiter=',', header=header_txt)

# fft
def get_fft(split_data, sample_rate):
    num_channels = np.shape(split_data)[0]
    num_samples = np.shape(split_data)[1]
    # freqs = fft.fftfreq(num_samples) * sample_rate
    freqs = np.linspace(0, 1, num_samples) * sample_rate

    split_data_fft = np.fft.fft(np.array(split_data)) * 1.0/sample_rate
    return freqs, split_data_fft

# plot FFT
def plot_fft(split_data, sample_rate, title="FFT Magnitude", color='b'):
    num_channels = np.shape(split_data)[0]
    num_samples = np.shape(split_data)[1]
    freqs_BT, fft_BT = get_fft(split_data, sample_rate)
    fig, axs = plt.subplots(num_channels, 1, sharex=True)
    fig.suptitle(title)
    fig.set_figwidth(6)
    fig.set_figheight(8)
    for i in np.arange(num_channels):
        axs[i].set_ylabel("ch" + str(i+1))
        axs[i].set_xlabel("Frequency (Hz)")
        axs[i].plot(freqs_BT[0:int(num_samples/2)],abs(fft_BT[i][0:int(num_samples/2)]), color=color)
        # axs[i].legend(["ch " + str(i+1)])
    for ax in axs:
        ax.label_outer()


# filters
def apply_filter(split_data, b, a):
    num_channels = np.shape(split_data)[0]
    split_data_filtered = np.copy(split_data)
    for i in range(0, num_channels):
        split_data_filtered[i] = signal.filtfilt(b, a, split_data_filtered[i])
    return split_data_filtered

def moving_avg(window_size):
    b = 1.0/window_size * np.ones(window_size)
    a = [1]
    return b, a

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='bandpass')
    return b, a

def butter_bandstop(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='bandstop')
    return b, a

def iir_notch(f0, Q, fs):
    b, a = signal.iirnotch(f0, Q, fs)
    return b, a

# remove body noise
# noise start, end: in seconds
def remove_body_noise(split_data, noise_start, noise_end, fs): 
    noise_data = split_data[:, noise_start:noise_end]
    split_data_len = np.shape(split_data)[1]

    # extend noise data
    a = np.shape(split_data)[1]
    b = np.shape(noise_data)[1]
    tiling_N = np.floor(a/b)

    noise_data = (np.tile(noise_data, tiling_N))
    # noise_data = noise_data[:,0:split_data_len]
    noise_fft = fft.fft(noise_data)
    noise_len = np.shape(noise_data)[1]

    noiseless_data = np.zeros(np.shape(split_data))
    i = 0
    while i+noise_len < noise_len:
        temp = split_data[:,i:i+noise_len]
        noiseless_data[:,i:i+noise_len] = fft.ifft(fft.fft(temp) - np.abs(noise_fft))
    
    return noiseless_data

## helper functions
def the_works_iir(split_data, fs, notch=60, Q=0.1, low=10, high=300): 
    # split_data = int_to_millivolts(split_data)
    b1, a1 = butter_bandpass(low, high, fs)
    split_data = apply_filter(split_data, b1, a1)
    b2, a2 = iir_notch(notch, Q, fs)
    split_data = apply_filter(split_data, b2, a2)
    return split_data

def plot_split_data(split_data, fs, filtered=False, title="Signal", color='b'):
    # Plot Unfiltered
    sample_rate = fs
    time = np.arange(np.shape(split_data)[1]) * 1/sample_rate
    num_channels = np.shape(split_data)[0]
    fig = plt.figure()
    gs = fig.add_gridspec(num_channels, hspace=0)
    axs = gs.subplots(sharex=True, sharey=True)
    fig.suptitle(title)

    for i in np.arange(num_channels):
        axs[i].plot(time,split_data[i], color=color)
        axs[i].set_xlabel("Time (s)")
        axs[i].set_ylabel("mV")

    # Hide x labels and tick labels for all but bottom plot.
    for ax in axs:
        ax.label_outer()
    
    plt.show()

# # mcv (unfinished, TODO)
# def plot_mcv(split_data, sample_rate, channel_a_num, channel_b_num, 
#         physical_dist_btwn_channels=1, 
#         height=150, distance=10, prominence=1, plot_peaks=False, 
#         max_time_btwn_peaks_ms=10):
    
#     max_dist_btwn_peaks = int(max_time_btwn_peaks_ms/sample_rate)

#     # create array of RMS vs time, subtract RMS from 

#     # for now just plot peaks
#     a = split_data[channel_a_num-1]
#     b = split_data[channel_b_num-1]
#     b_size = np.size(b)
#     if (np.size(a) > b_size):
#         a = a[0:b_size]

#     peaks_a, _ = signal.find_peaks(a, height=height, distance=distance, 
#             prominence=prominence)
#     peaks_b, _ = signal.find_peaks(b, height=height, distance=distance, 
#             prominence=prominence)
#     times = (peaks_a*(1.0/sample_rate))
#     mcv = np.zeros_like(peaks_a)

#     # b_idx = 0
#     # mcv_idx = 0
#     # for a_idx in peaks_a:
#     #     delta_t = peaks_b[b_idx] - a_idx
#     #     while (delta_t < 0):
#     #         b_idx += 1
#     #         if b_idx > (b_size-1):
#     #             return times, mcv 
#     #         else:
#     #             delta_t = peaks_b[b_idx] - a_idx
          
#     #     if delta_t == 0:
#     #         mcv[mcv_idx] = physical_dist_btwn_channels*sample_rate
#     #     elif delta_t < max_dist_btwn_peaks:
#     #         mcv[mcv_idx] = physical_dist_btwn_channels/delta_t * sample_rate
#     #     mcv_idx += 1

#     if plot_peaks:
#         f, axs = plt.subplots(2,1, sharex='all', sharey='all')
#         axs[0].plot(a)
#         axs[0].plot(peaks_a, a[peaks_a], "x")
#         axs[0].plot(np.zeros_like(a), "--", color="gray")
#         axs[0].set_title("peaks ch a")

#         axs[1].plot(b)
#         axs[1].plot(peaks_b, b[peaks_b], "x")
#         axs[1].plot(np.zeros_like(b), "--", color="gray")
#         axs[1].set_title("peaks ch b")
#         plt.show()

#     # plt.figure()
#     # plt.plot(times, mcv)
#     # plt.title("MCV of Channel " + str(channel_a_num) + " and " + str(channel_b_num))
#     # plt.xlabel("time")
#     # plt.show()

#     return times, mcv

# main
def main():
    return

if __name__ == "__main__":
    main()
