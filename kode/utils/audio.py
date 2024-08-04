from librosa.feature import melspectrogram, mfcc, chroma_stft
from librosa.feature import spectral_centroid, zero_crossing_rate
from librosa.core import power_to_db
from librosa import get_duration
from librosa.util import normalize
from numpy import min, max
from scipy.signal import find_peaks
from torch import tensor
from numpy import ndarray


def normalize_audio(audio):
    return normalize(audio, axis=0)


def split_audio(y, sr, duration):

    segment_len = int(duration * sr)

    segments = []

    for i in range(0, len(y), segment_len):
        segment = y[i:i+segment_len]
        if len(segment) == segment_len:
            segments.append(segment)

    return segments


def audio_min_max_duration(signals, sr):
    durations = []
    for i in range(len(signals)):
        duration = get_duration(y=signals[i], sr=sr)
        durations.append(duration)

    return min(durations), max(durations)


def extract_mel(y, sr):

    if not isinstance(y, ndarray):
        y = y.numpy()

    spectrogram = melspectrogram(
        y=y,
        sr=sr,
        n_fft=sr,
        hop_length=sr // 2
    )

    spectrogram = power_to_db(spectrogram, ref=max)

    return tensor(spectrogram)


def extract_mfcc(y, sr):

    if not isinstance(y, ndarray):
        y = y.numpy()

    mfccs = mfcc(y=y, sr=sr)

    return tensor(mfccs)


def extract_zcr(y, sr):

    if not isinstance(y, ndarray):
        y = y.numpy()

    zcr = zero_crossing_rate(
        y=y,
        frame_length=sr,
        hop_length=sr // 2
    )

    return tensor(zcr)


def extract_centroid(y, sr):

    if not isinstance(y, ndarray):
        y = y.numpy()

    centroid = spectral_centroid(
        y=y,
        sr=sr,
        n_fft=sr,
        hop_length=sr // 2
    )

    return tensor(centroid)


def extract_chroma(y, sr):

    if not isinstance(y, ndarray):
        y = y.numpy()

    chroma = chroma_stft(
        y=y,
        sr=sr,
        n_fft=sr,
        hop_length=sr // 2
    )

    return tensor(chroma)


def extract_peaks(y):

    if not isinstance(y, ndarray):
        y = y.numpy()

    peaks, _ = find_peaks(x=y)

    return tensor(peaks)
