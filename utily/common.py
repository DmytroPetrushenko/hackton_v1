from constants import MESSAGE_FOLDER


def create_message_from_file(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file_reader:
            lines = file_reader.readlines()
            filtered_lines = [line.replace('\n', '') for line in lines]
            return ' '.join(filtered_lines)
    except FileNotFoundError:
        print(f"A file was not found according to this file name: {file_path}.")