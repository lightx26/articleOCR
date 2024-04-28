import queue
import time
from threading import Thread

import winsound


class AudioThread(Thread):
    def __init__(self, audio_queue, export_thread_finished_event, start_time=0):
        super().__init__()
        self.buffer_audio = audio_queue
        self.export_finished_event = export_thread_finished_event
        self.start_time = start_time

    def run(self):
        while not (self.export_finished_event.is_set() and self.buffer_audio.empty()):
            try:
                audio_path = self.buffer_audio.get()
                print("Start playing audio after: ", time.time() - self.start_time, "s", sep="")
                winsound.PlaySound(audio_path, winsound.SND_FILENAME)
            except queue.Empty:
                pass
