import requests
import json


def write_text(output_path, text):
    with open(output_path, 'a', encoding='utf-8') as f:
        f.write(text)


def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return "\n".join(f.readlines())


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