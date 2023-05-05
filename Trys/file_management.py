import atexit
import os
import tempfile
import shutil
import zipfile

from halo import halo
from pydub import AudioSegment
from tqdm import tqdm

from Trys.utils import format_timestamp


def create_tmp_dir():
    temp_dir = tempfile.mkdtemp()

    def clear_temp_dir():
        shutil.rmtree(temp_dir)

    atexit.register(clear_temp_dir)

    return temp_dir


def extract_sources_from_input_paths(input_paths):
    temp_dir = create_tmp_dir()
    os.mkdir(f"{temp_dir}/src")

    for input_path in input_paths:
        extract_source_files(input_path, temp_dir)

    return temp_dir


@halo.Halo(text='Extracting source files', spinner='dots')
def extract_source_files(input_path, temp_dir):
    if os.path.isfile(input_path):
        if zipfile.is_zipfile(input_path):
            process_zip(input_path, temp_dir)
        else:
            process_single_file(input_path, temp_dir)
    elif os.path.isdir(input_path):
        process_directory(input_path, temp_dir)
    else:
        print(f"Error: Invalid input path: {input_path}")


def process_zip(zip_file, temp_dir):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(f"{temp_dir}/src")


def process_single_file(file_path, temp_dir):
    shutil.copy(file_path, f"{temp_dir}/src/{os.path.basename(file_path)}")


def process_directory(input_path, temp_dir):
    for root, _, filenames in os.walk(input_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            process_single_file(file_path, temp_dir)


def create_clips_dir():
    temp_dir = create_tmp_dir()
    os.mkdir(f"{temp_dir}/clips")

    return temp_dir


def load_audio(root, file_name):
    return AudioSegment.from_file(os.path.join(root, file_name))


def walk_src_files(temp_dir):
    return os.walk(f"{temp_dir}/src")


def export_transcript(all_transcribed_clips, output_path, mode):
    with open(output_path, "w", encoding="utf-8") as f:
        for (start, end), speaker, text, _, interjection, crosstalk, _ in tqdm(all_transcribed_clips, desc=f"Saving final transcript to {output_path}", unit="scripts"):
            if mode != 'embed' or not interjection:
                f.write(f"{format_timestamp(start)} - {format_timestamp(end)} ({speaker}){insert_tag(interjection, crosstalk, mode)}: {text}\n")


def insert_tag(interjection, crosstalk, mode):
    if interjection and mode == 'tag':
        return " [interjection]"
    elif crosstalk and (mode == 'tag' or mode == 'embed'):
        return " [crosstalk]"
    else:
        return ""
