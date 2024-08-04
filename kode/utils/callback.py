import os
from kode.utils.io_util import *

from tensorflow.keras import callbacks  # type: ignore


def get_callbacks(save: bool, fold: int, root_dir: str, csv_append: bool):
    if not save:
        return []

    if not dir_exists(root_dir):
        create_dir(root_dir)

    if not root_dir.endswith("/"):
        root_dir += "/"

    mdl_chkpt_name = f"model_f_{fold}_ta_{{accuracy:.5f}}_va_{{val_accuracy:.5f}}.h5"

    cbks = [
        callbacks.ModelCheckpoint(
            filepath=root_dir + "model_chkpoint/" + mdl_chkpt_name,
            save_best_only=True,
            save_weights_only=False,
            monitor="val_accuracy",
            mode="max",
            verbose=1,
        ),
        callbacks.CSVLogger(
            filename=root_dir + f"training_logs.csv",
            separator=",",
            append=csv_append,
        ),
        callbacks.EarlyStopping(
            monitor="val_accuracy",
            patience=20,
            verbose=1,
            mode="max",
            restore_best_weights=False,
        ),
    ]

    return cbks
