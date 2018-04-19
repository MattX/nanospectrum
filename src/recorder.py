import pyaudio
import wave

CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1


class MikeRecorder:
    def record(self, queue, rate):
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=rate,
                        input=True,
                        frames_per_buffer=CHUNK)

        while True:
            data = stream.read(CHUNK)
            queue.put_nowait(data)


class FileRecorder:
    def __init__(self, file):
        self.file = file

    def record(self, queue, rate):
        p = pyaudio.PyAudio()

        stream = wave.open(self.file, 'rb')
        assert p.get_format_from_width(stream.getsampwidth()) == FORMAT
        out = p.open(format=p.get_format_from_width(stream.getsampwidth()),
                     channels=stream.getnchannels(),
                     rate=stream.getframerate(),
                     output=True)

        data = stream.readframes(CHUNK)

        while data != b'':
            out.write(data)
            queue.put_nowait(data)
            data = stream.readframes(CHUNK)
