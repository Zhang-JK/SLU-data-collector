import time

import pyaudio
import numpy as np
import threading
from queue import Queue
from scipy.io.wavfile import write


class Recoder:
    def __init__(self, frames_per_buffer=3200, format=pyaudio.paInt16, channels=1, rate=16000):
        self.frames_per_buffer = frames_per_buffer
        self.format = format
        self.channels = channels
        self.rate = rate
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            output=False,
            frames_per_buffer=self.frames_per_buffer
        )
        self.stream.stop_stream()
        self.op_queue = Queue()
        self.op_thread = threading.Thread(target=self.__rec_thread)
        self.op_thread.start()
        self.is_recording = False

    def __rec_thread(self):
        while True:
            cmd = self.op_queue.get()
            if cmd["op"] == "terminate":
                break
            if cmd["op"] == "start":
                frames = []
                name = cmd["name"]
                self.stream.start_stream()
                while True:
                    data = self.stream.read(self.frames_per_buffer)
                    frames.append(data)
                    if not self.op_queue.empty():
                        cmd = self.op_queue.get(False)
                        if cmd is not None and cmd["op"] == "stop":
                            write(name, self.rate, np.frombuffer(b''.join(frames), dtype=np.int16))
                            self.stream.stop_stream()
                            break

    def start(self, name):
        if self.is_recording:
            return
        self.is_recording = True
        self.op_queue.put({"op": "start", "name": name})

    def stop(self):
        if not self.is_recording:
            return
        self.is_recording = False
        self.op_queue.put({"op": "stop"})

    def close(self):
        if self.is_recording:
            self.stop()
        self.op_queue.put({"op": "terminate"})
        time.sleep(1)
        self.op_thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
