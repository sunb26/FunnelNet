import argparse
from datetime import datetime

import numpy as np
from keras import optimizers
from tensorflow import saved_model

from kode.data.datagen import HeartSoundDataGenerator
from kode.model.model import get_model
from kode.utils.callback import get_callbacks
from kode.utils.core_util import manual_seed
from kode.utils.data_util import *
from kode.utils.filter import *
from kode.utils.io_util import *
from kode.utils.sig_util import *
from kode.utils.tflite import tf_lite_model

_DATASET = ["bently", "cinc", "circor", "synthetic"]
_RD_SEED = 13
_RESAMPLING_RATE = 1000
_CBK_ROOT = "callbacks"
_DS_ROOT = "dataset"
_SAVED_DIR = "keras_model"
_TFLITE_DIR = "tflite_model"

if __name__ == "__main__":

    manual_seed(_RD_SEED)

    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--dataset", type=str, required=True, choices=_DATASET, help="Dataset name.")
    parser.add_argument("-f", "--fold", type=int, default=10, help="Number of CV fold.")
    parser.add_argument("-e", "--epoch", type=int, default=20, help="Number of epoch.")
    parser.add_argument("-b", "--batch", type=int, default=32, help="Batch size.")
    parser.add_argument("-r", "--record", action="store_true", help="Record callback.")
    parser.add_argument("-a", "--append", action="store_true", help="Append to CSV.")
    parser.add_argument( "-l", "--lite", action="store_true", help="Prepare TFLite model.")
    parser.add_argument( "-c", "--clean", action="store_true", help="Perform a clean run.")
    parser.add_argument( "-v", "--verbose", action="store_true", help="Whether to print info.")

    args = parser.parse_args()

    if args.clean:
        c_path = f"{_CBK_ROOT}/{args.dataset}"
        if dir_exists(c_path):
            clear_dir(c_path)
            print(f"Cleaned {c_path}...")
        else:
            print(f"{c_path} does not exist...")

    db_path = f"{_DS_ROOT}/{args.dataset}/"
    generator = HeartSoundDataGenerator(args.dataset, db_path)
    data = generator.get_data()

    audio_data = np.array(data[0])
    label_data = np.array(data[1]).astype(np.float32)

    signals = extract_audio_data(audio_data, _RESAMPLING_RATE)

    signals = extract_signals(signals)

    signals, label_data = remove_inconsistent_signals(signals, label_data)

    signals = np.array(signals)

    print("Removing outliers...")
    signals = remove_outliers(signals, 3)

    print("Filtering signals...")
    signals = bp_butter_filter(signals, _RESAMPLING_RATE, 2, 500, 20)

    print(f"Data shape: {signals.shape}")

    feat_data = (signals - np.min(signals)) / (np.max(signals) - np.min(signals))

    label_data = np.array(label_data)

    features, labels = smote(feat_data, label_data, _RD_SEED)

    folds = skf(args.fold, features, labels, _RD_SEED)

    i_shape = features.shape[1:]
    unique_labels = np.unique(labels)
    n_classes = 1 if len(unique_labels) == 2 else len(unique_labels)
    loss_fn = ("binary_crossentropy" if n_classes == 1 else "sparse_categorical_crossentropy")

    model = get_model(i_shape, n_classes)

    optim = optimizers.Adam(learning_rate=0.001)

    model.compile(optimizer=optim, loss=loss_fn, metrics=["accuracy"])

    if args.verbose:
        model.summary()

    cbk_dir = f"{_CBK_ROOT}/{args.dataset}"

    vbs = 1 if args.verbose else 0

    start_time = datetime.now()
    print(f"Start time: {start_time}\n")

    for i, (train_ids, val_ids) in enumerate(folds):
        print("Training on fold " + str(i + 1) + f"/{args.fold}...\n")

        Xtrain_data = features[train_ids]
        Xval_data = features[val_ids]
        ytrain_data = labels[train_ids]
        yval_data = labels[val_ids]

        model.fit(
            Xtrain_data,
            ytrain_data,
            epochs=args.epoch,
            verbose=vbs,
            shuffle=True,
            batch_size=args.batch,
            callbacks=get_callbacks(args.record, i, cbk_dir, args.append),
            validation_data=(Xval_data, yval_data),
            use_multiprocessing=True,
            workers=8,
        )

    end_time = datetime.now()
    print(f"\nEnd time: {end_time}")

    print("Saving runtime info...")

    with open(f"{_CBK_ROOT}/{args.dataset}/runtime.txt", "w") as f:
        f.write(f"Start time: {start_time}\n")
        f.write(f"End time: {end_time}\n")
        f.write(f"Total time: {end_time - start_time}\n")
        f.write(f"Epochs: {args.epoch}\n")
        f.write(f"Batch size: {args.batch}\n")
        f.write(f"Fold: {args.fold}\n")
        f.write(f"Random seed: {_RD_SEED}\n")

    print("Saved runtime info...")

    print("Saving model...")

    saved_model_dir = f"{_CBK_ROOT}/{args.dataset}/{_SAVED_DIR}"

    if not dir_exists(saved_model_dir):
        create_dir(saved_model_dir)
    else:
        clear_dir(saved_model_dir)

    saved_model.save(model, saved_model_dir)

    print("Saved model...")

    if args.lite:
        print("Preparing TFLite model...")

        tflite_model = tf_lite_model(features, saved_model_dir)

        tflite_save_path = f"{_CBK_ROOT}/{args.dataset}/{_TFLITE_DIR}/"
        tflite_model_name = "model.tflite"

        if not dir_exists(tflite_save_path):
            create_dir(tflite_save_path)

        with open(tflite_save_path + tflite_model_name, "wb") as f:
            f.write(tflite_model)

        print("Saved TFLite model...")
