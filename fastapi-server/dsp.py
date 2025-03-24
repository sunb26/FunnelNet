import io
import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wav

def fir1(order, low, high=None):
    if high is None:
        taps = signal.firwin(order + 1, low, window='hamming')
    else:
        taps = signal.firwin(order + 1, [low, high], pass_zero=False, window='hamming')
    return taps

def apply_filter(signal_data, coeffs):
    return signal.lfilter(coeffs, 1.0, signal_data)

def normalize(signal_data):
    max_val = np.max(np.abs(signal_data))
    return signal_data / max_val if max_val != 0 else signal_data

def write_wav(signal_data, sample_rate):
    scaled_signal = np.int16(signal_data * 32767)  # Convert to int16
    output_stream = io.BytesIO()
    wav.write(output_stream, sample_rate, scaled_signal)
    output_stream.seek(0) # Reset the stream position to beginnning
    return output_stream

def trim(sample_rate, signal_data, trim_length):
    remove = sample_rate * trim_length
    if len(signal_data) <= sample_rate * trim_length:
        print("Error: File is too short to cut x seconds")
        return signal_data
    
    new_data = signal_data[remove:]
    return new_data


async def dsp(raw_audio: io.BytesIO):
    print("Starting DSP processing...")
    
    raw_audio.seek(0) # ensure stream position is at the beginning

    sample_rate, signal_data = wav.read(raw_audio,  mmap=False)
    
    # Ensure signal is float
    signal_data = signal_data[:len(signal_data)]

    if signal_data.dtype != np.float32:
        signal_data = signal_data.astype(np.float32) / np.iinfo(signal_data.dtype).max

    signal_data = trim(sample_rate,signal_data, 2) #last parameter is number of sec to remove
    
    # Define bandpass filter parameters
    Fl, Fh = 10.0, 200.0
    WcL, WcH = Fl / (sample_rate / 2), Fh / (sample_rate / 2)  # Normalize cutoff frequencies
    
    # Design FIR bandpass filter
    order = 1024
    bbp = fir1(order, WcL, WcH)
    
    # Apply bandpass filter
    filtered_signal = apply_filter(signal_data, bbp)
    
    # Normalize the amplified signal
    amplified_signal = normalize(filtered_signal)
    
    # Apply low-pass smoothing filter
    lp_filter = fir1(128, 0.1)
    smoothed_signal = apply_filter(amplified_signal, lp_filter)
    
    return write_wav(smoothed_signal, sample_rate)