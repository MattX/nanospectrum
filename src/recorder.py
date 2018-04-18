import pyaudio


def record(queue, rate):
    CHUNK = 128
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=rate,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    while True:
        data = stream.read(CHUNK)
        queue.put_nowait(data)
