import os
import queue
import threading
from pathlib import Path
from AppThread.AudioThread import AudioThread
from utils import FileHandler


class ExportThread(threading.Thread):
    def __init__(self, output_path, text_queue, read_thread_finished_event, start_time=0):
        super().__init__()
        self.output_path = output_path
        self.buffer_text = text_queue
        self.read_finished_event = read_thread_finished_event
        self.export_finished_event = threading.Event()
        self.start_time = start_time

    def run(self):
        audio_queue = queue.Queue()
        audio_thread = AudioThread(audio_queue, self.export_finished_event, self.start_time)
        audio_thread.start()

        line_idx = 0
        while not (self.read_finished_event.is_set() and self.buffer_text.empty()):
            try:
                text = self.buffer_text.get(timeout=1)

                # Export text file
                FileHandler.write_text(self.output_path + ".txt", text + "\n")
                # Export audio file
                os.makedirs(os.path.join(Path(self.output_path).parent.parent, "audio", os.path.basename(self.output_path)), exist_ok=True)
                des_name = os.path.join(Path(self.output_path).parent.parent, "audio", os.path.basename(self.output_path), f"line_{line_idx}.wav")
                FileHandler.generate_audio("hn-phuongtrang", text, des_name)
                audio_queue.put(des_name)

                line_idx += 1

            except queue.Empty:
                pass

        self.export_finished_event.set()

        audio_thread.join()