import os

import numpy as np

from ..utils.file_util import rename_duplicates
from ..utils.io_util import file_exists

_LABEL_MAP = {"Absent": 0, "Present": 1, "Unknown": 2}


def generate_circor_data(path):
    X = []
    y = []

    csv_path = os.path.join(path, "training_data.csv")
    csv_data = np.loadtxt(csv_path, dtype=str, delimiter=",", skiprows=1)

    patient_ids = csv_data[:, 0].tolist()
    recording_locs = csv_data[:, 1].tolist()
    labels = csv_data[:, 7].tolist()

    for i in range(len(recording_locs)):
        r_locs = recording_locs[i].split("+")
        r_locs = rename_duplicates(r_locs, "_")
        for loc in r_locs:
            record_path = os.path.join(path, f"{str(patient_ids[i])}_{loc}.wav")
            if not file_exists(record_path):
                print(r_locs)
                raise FileNotFoundError(f"File {record_path} not found.")
            X.append(record_path)
            y.append(labels[i])

    y = [_LABEL_MAP[i] for i in y]

    return X, y
