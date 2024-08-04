import tflite_runtime.interpreter as tflite
from scipy.io import wavfile
import scipy.signal as scipy_sig
import numpy as np
from scipy.signal import butter, lfilter
from glob import glob

_RESAMPLING_RATE = 1000

def get_audio_files(dir):
    return glob(f"{dir}/*.wav")

def convert_audio(file, target_sr=None):
    _, sig = wavfile.read(file)
    sig = np.float64(sig)
    np.divide(sig, np.float64(32768), out=sig)

    if target_sr is not None:
        assert target_sr > 0, "Target sampling rate must be positive."
        sig = scipy_sig.resample(x=sig, num=target_sr)

    return sig


def compute_cwt(data, window=32):
    widths = np.geomspace(1, window, window)

    sig = scipy_sig.cwt(data, scipy_sig.morlet2, widths).T
    sig = np.abs(sig)
    sig = sig.reshape(sig.shape[0], sig.shape[1], 1)

    return sig


def remove_outliers(audio, patience):
    threshold = np.mean(audio) + patience * np.std(audio)
    return np.where(audio > threshold, threshold, audio)


def bp_butter_filter(y, sr, order, highcut, lowcut):
    sample_rate = sr
    lowcut = lowcut / (sample_rate / 2)
    highcut = highcut / (sample_rate / 2)

    b, a = butter(
        N=order,
        Wn=[lowcut, highcut],
        btype="bandpass",
        analog=True,
    )

    y = lfilter(b, a, y)

    return y


def prepare_data(file):
    sig = convert_audio(file, _RESAMPLING_RATE)
    sig = compute_cwt(sig)
    sig = remove_outliers(sig, 3)
    sig = bp_butter_filter(sig, _RESAMPLING_RATE, 2, 500, 20)

    return sig


if __name__ == "__main__":

    mdl_path = "models/bently.tflite"
    audio_files_dir = "audio"

    interpreter = tflite.Interpreter(model_path=mdl_path)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    print("Input details:", input_details)
    print("Output details:", output_details)

    audio_files = get_audio_files(audio_files_dir)

    for file in audio_files:
        data = prepare_data(file)
        data = data.astype(np.float32)
        data = np.expand_dims(data, axis=0)

        interpreter.set_tensor(input_details[0]['index'], data)
        interpreter.invoke()

        output_data = interpreter.get_tensor(output_details[0]['index'])
        print(f"File: {file}, Output: {output_data}")
