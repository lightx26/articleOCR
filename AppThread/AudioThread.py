import queue
from threading import Thread

import winsound


class AudioThread(Thread):
    def __init__(self, audio_queue, export_thread_finished_event):
        super().__init__()
        self.buffer_audio = audio_queue
        self.finished_event = export_thread_finished_event


    def run(self):
        while not (self.finished_event.is_set() and self.buffer_audio.empty()):  # Check for export_thread completion
            try:
                audio_path = self.buffer_audio.get(timeout=1)  # Non-blocking queue access
                winsound.PlaySound(audio_path, winsound.SND_FILENAME)
            except queue.Empty:
                pass
