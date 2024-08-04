from .bently import generate_bently_data
from .chs import generate_chs_data
from .cinc import generate_cinc_data
from .circor import generate_circor_data
from .synthetic import generate_synthetic_data


class HeartSoundDataGenerator:
    def __init__(self, db, path):
        self._db = db
        self._path = path

    def get_data(self):
        X, y = [], []

        if self._db == "cinc":
            X, y = generate_cinc_data(self._path)
        elif self._db == "circor":
            X, y = generate_circor_data(self._path)
        elif self._db == "synthetic":
            X, y = generate_synthetic_data(self._path)
        elif self._db == "chs":
            X, y = generate_chs_data(self._path)
        elif self._db == "bently":
            X, y = generate_bently_data(self._path)
        else:
            raise NotImplementedError

        y = [int(i) for i in y]

        return X, y
