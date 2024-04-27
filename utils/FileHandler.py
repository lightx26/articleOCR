import os


def write_text(output_path, filename, text):
    with open(os.path.join(output_path, filename), 'w', encoding='utf-8') as f:
        f.write(text)


def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return "\n".join(f.readlines())