from utilities import *
import os

def main():
    NUM_CHANNELS = 8

    file_path_list = [
        r"sample_7_keysight_edu3321a\20220608_1745_59000_ms.txt",
        r"sample_7_keysight_edu3321a\20220608_1747_60000_ms.txt",
        r"sample_7_keysight_edu3321a\20220608_1835_61000_ms.txt",
        r"sample_7_keysight_edu3321a\20220608_1837_62000_ms.txt",
        r"sample_7_keysight_edu3321a\20220608_1840_63000_ms.txt",
        r"sample_7_keysight_edu3321a\20220608_1842_64000_ms.txt",
        r"sample_7_keysight_edu3321a\20220608_1843_65000_ms.txt",
        r"sample_7_keysight_edu3321a\20220608_1844_66000_ms.txt",
        r"sample_7_keysight_edu3321a\20220608_1845_66000_ms.txt",
        r"sample_7_keysight_edu3321a\20220608_1847_70000_ms.txt",
        r"sample_7_keysight_edu3321a\20220608_1848_70000_ms.txt",
        r"sample_7_keysight_edu3321a\20220608_1857_72000_ms.txt",
        r"sample_7_keysight_edu3321a\20220608_1903_75000_ms.txt",
        r"sample_7_keysight_edu3321a\20220608_1905_80000_ms.txt",
        r"sample_7_keysight_edu3321a\20220608_1906_80000_ms.txt",
        r"sample_7_keysight_edu3321a\20220608_1918_80000_ms.txt",
        r"sample_7_keysight_edu3321a\20220608_1920_81000_ms.txt",
        r"sample_7_keysight_edu3321a\20220608_1923_82000_ms.txt",
    ]

    for file_path in file_path_list:
        new_file_path = file_path.replace(".txt", "_formatted.txt")
        data = raw_file_to_array(file_path)
        split_data = split_data_into_channels(data, NUM_CHANNELS)
        save_split_data_as_csv(split_data, new_file_path, NUM_CHANNELS, 1000)
    
if __name__ == "__main__":
    main()



