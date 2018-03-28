# PyAudio回调方式录音
import pyaudio
import numpy as np
import time

pa = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, flag):
    audio_data = np.fromstring(in_data, dtype=np.float32)
    # Instead of printing, process here the audio chunk 'audio_data' with libROSA
    # [...]
    print(type(audio_data), audio_data.shape)   # audio_data: 'numpy.ndarray',(512,); in_data: 'bytes', 2048
    return None, pyaudio.paContinue

stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=16000,
                 output=False,
                 input=True,
                 stream_callback=callback)

stream.start_stream()
# wait for stream to finish
while stream.is_active():
    time.sleep(0.25)

stream.stop_stream()
stream.close()
pa.terminate()