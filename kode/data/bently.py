import glob
import os

from ..utils.io_util import file_exists

_LABEL_MAP = {
    "artifact": 0,
    "extrahs": 1,
    "extrasystole": 2,
    "murmur": 3,
    "normal": 4,
}


def generate_bently_data(path):
    dir = os.listdir(path)

    X = []
    y = []

    for d in dir:
        sub_dir = os.path.join(path, d)
        for c in os.listdir(sub_dir):
            sub_sub_dir = os.path.join(sub_dir, c)
            wav_files = glob.glob(sub_sub_dir + "/*.wav")
            for f in wav_files:
                assert file_exists(f), f"File {f} not found."
                X.append(f)
                y.append(c)

    y = [_LABEL_MAP[i] for i in y]

    assert len(X) == len(y), "X and y must have the same length."

    return X, y
