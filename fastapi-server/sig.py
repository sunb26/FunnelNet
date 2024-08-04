import numpy as np
import scipy.signal as scipy_sig
from scipy.io import wavfile

from filter import *


async def preprocess_audio(file_path: str) -> np.ndarray:

    resampling_rate = 1000

    _, audio = wavfile.read(file_path)

    audio = np.float64(audio)
    np.divide(audio, np.float64(32768), out=audio)

    audio = scipy_sig.resample(x=audio, num=resampling_rate)

    window = 32
    widths = np.geomspace(1, window, window)

    audio = scipy_sig.cwt(audio, scipy_sig.morlet2, widths).T
    audio = abs(audio)
    audio = audio.reshape(audio.shape[0], audio.shape[1], 1)

    audio = remove_outliers(audio, 3)
    audio = bp_butter_filter(audio, resampling_rate, 2, 500, 20)

    return audio