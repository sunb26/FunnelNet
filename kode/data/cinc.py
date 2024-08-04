import glob
import os

import numpy as np


def generate_cinc_data(path):
    dir = os.listdir(path)

    X = []
    y = []

    for d in dir:
        sub_dir = os.path.join(path, d)
        if os.path.isdir(sub_dir):
            wav_file_paths = []
            wav_files = glob.glob(sub_dir + "/*.wav")
            for f in wav_files:
                wav_file_paths.append(f)
            X.extend(wav_file_paths)

            label_file = np.loadtxt(
                sub_dir + "/REFERENCE.csv", dtype=str, delimiter=","
            )
            labels = label_file[:, 1].tolist()

            assert len(wav_file_paths) == len(
                labels
            ), "Number of wav files and labels do not match"

            y.extend(labels)

    y = [0 if i == "-1" else i for i in y]

    return X, y
