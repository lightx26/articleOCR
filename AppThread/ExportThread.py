import queue
import threading
import time

import winsound
import requests
import json

from AppThread.AudioThread import AudioThread


class ExportThread(threading.Thread):
    def __init__(self, nqueue, read_thread_finished_event, begin_time=0):
        super().__init__()
        self.buffer_text = nqueue
        self.finished_event = read_thread_finished_event
        self.begin_time = begin_time
        self.finished_event = threading.Event()

    def run(self):
        line_idx = 0
        audio_queue = queue.Queue()
        audio_thread = AudioThread(audio_queue, self.finished_event)
        audio_thread.start()
        while not (self.finished_event.is_set() and self.buffer_text.empty()):  # Check for read_thread completion
            try:
                text = self.buffer_text.get(timeout=1)  # Non-blocking queue access
                des_name = f"data/output/tmp_{line_idx}.wav"
                generate_audio("hn-phuongtrang", text, des_name)
                audio_queue.put(des_name)
                # print("Start playing audio: ", time.time() - self.begin_time)
                # winsound.PlaySound("data/output/tmp.wav", winsound.SND_FILENAME)
            except queue.Empty:
                pass  # Handle empty queue gracefully

        print("Read thread finished, export thread exiting.")
        self.finished_event.set()

def generate_audio(voice, text, des_name):
    url = "https://viettelgroup.ai/voice/api/tts/v1/rest/syn"
    data = {
        "text": text,
        "voice": voice,
        "id": "2",
        "without_filter": False,
        "speed": 1.0,
        "tts_return_option": 2
    }
    headers = {'Content-type': 'application/json',
               'token': 'dw1EEOdB48eqoIvopUZwOuT-gkZ4zzrvGHNIuVzPTlnAkUUiPWnUN-yTPJtZSNo2'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:

        data = response.content
        # Thay localpath
        file_path = f"{des_name}"  # thay path
        with open(file_path, "wb") as file:
            file.write(data)

    else:
        print("Không thể tạo file âm thanh. Mã trạng thái:", response.status_code)
