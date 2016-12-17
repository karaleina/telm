#!/usr/bin/python

def complement_of_two_12_bit(raw_value):
    sign_bit = (raw_value & 0x800) >> 11
    rest = raw_value & 0x7ff
    return -2048 * sign_bit + rest

def read_samples(dat_file_name):

    samples = []

    with open(dat_file_name, "rb") as f:
        while True:
            sample = f.read(3)
            if not sample:
                break
            sample_bytes = [ord(char) for char in sample]
            first_value = complement_of_two_12_bit(sample_bytes[0] | ((sample_bytes[1] & 0x0f) << 8))
            second_value = complement_of_two_12_bit(sample_bytes[2] | ((sample_bytes[1] & 0xf0) << 4))

            samples.append((first_value, second_value))

    return samples

samples_from_file = read_samples("downloads/s20011.dat")

for first_channel_value, second_channel_value in samples_from_file:
    print(str(first_channel_value) + " " + str(second_channel_value))
