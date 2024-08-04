import os

import numpy as np

from ..utils.io_util import file_exists


def generate_synthetic_data(path):
    X = []
    y = []

    train_csv_path = os.path.join(path, "Train_set.csv")
    test_csv_path = os.path.join(path, "Test_set.csv")
    train_csv_data = np.loadtxt(train_csv_path, dtype=str, delimiter=",", skiprows=1)
    test_csv_data = np.loadtxt(test_csv_path, dtype=str, delimiter=",", skiprows=1)

    for i in range(train_csv_data.shape[0]):
        temp_file = os.path.join(path, train_csv_data[i][0])
        assert file_exists(temp_file), f"File {temp_file} not found."
        X.append(temp_file)
        y.append(train_csv_data[i][1])

    for i in range(test_csv_data.shape[0]):
        temp_file = os.path.join(path, test_csv_data[i][0])
        assert file_exists(temp_file), f"File {temp_file} not found."
        X.append(temp_file)
        y.append(test_csv_data[i][1])

    y = [0 if x == "-1" else x for x in y]

    return X, y
