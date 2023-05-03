#!/usr/bin/env python3

import tqdm

from Trys.audio_processing import load_transcription_model, detect_nonsilent_sections_from_audio, \
    create_audio_clips, transcribe_audio_clips
from Trys.cli_args import parse_arguments
from Trys.file_management import extract_sources_from_input_paths, load_audio, walk_src_files
from Trys.utils import merge_transcripts, extract_username, format_timestamp


def main():
    args = parse_arguments()

    input_paths, output_path, discord_usernames, experimental, min_silence_len, silence_thresh, transcription_model = (
        args["<input>"], args['--output'], args['--discord'], args['--experimental'], int(args['--min_silence_len']),
        int(args['--silence_thresh']), args['--transcription_model'])

    src_dir = extract_sources_from_input_paths(input_paths)

    model = load_transcription_model(transcription_model)

    all_transcribed_clips = []

    for root, _, files in walk_src_files(src_dir):
        for file_name in files:
            if file_name.lower().endswith(('.wav', '.mp3', '.flac', '.ogg')):
                speaker = extract_username(file_name, discord_usernames)

                audio = load_audio(root, file_name)
                nonsilent_sections = detect_nonsilent_sections_from_audio(audio, file_name, min_silence_len,
                                                                          silence_thresh)
                audio_clips = create_audio_clips(file_name, nonsilent_sections, audio)
                transcribed_clips = transcribe_audio_clips(audio_clips, model, speaker, min_silence_len, experimental)

                for (start, end), text in tqdm.tqdm(transcribed_clips, desc=f"Merging {speaker} transcript into final "
                                                                            f"transcript", unit="scripts"):
                    all_transcribed_clips = merge_transcripts(all_transcribed_clips, [((start, end), speaker, text)])

    with open(output_path, "w", encoding="utf-8") as f:
        for (start, end), speaker, text in tqdm.tqdm(all_transcribed_clips, desc=f"Saving final transcript to "
                                                                                 f"{output_path}", unit="scripts"):
            f.write(f"{format_timestamp(start)} - {format_timestamp(end)} ({speaker}): {text}\n")


if __name__ == "__main__":
    main()
