import glob
import os

from ..utils.io_util import file_exists


def generate_chs_data(path):
    dir = os.listdir(path)

    X = []
    y = []

    for d in dir:
        sub_dir = os.path.join(path, d)
        wav_files = glob.glob(sub_dir + "/*.wav")
        for f in wav_files:
            assert file_exists(f), f"File {f} not found."
            X.append(f)
            if d == "normal":
                y.append(0)
            elif d == "abnormal":
                y.append(1)

    assert len(X) == len(y), "X and y must have the same length."

    return X, y
