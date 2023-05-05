#!/usr/bin/env python3
from Trys.audio_processing import load_transcription_model, detect_nonsilent_sections_from_audio, \
    create_audio_clips, transcribe_audio_clips
from Trys.cli_args import parse_arguments, get_mode
from Trys.file_management import extract_sources_from_input_paths, load_audio, walk_src_files, export_transcript
from Trys.utils import merge_transcripts, extract_username, embed_interjections


def main():
    args = parse_arguments()

    input_paths = args["<input>"]
    mode = get_mode(args)

    output_path, discord_usernames, pause_len, db_silence_thresh, transcription_model, language = (
        args['--output'], args['--discord_usernames'], int(args['--pause_len']), int(args['--db_silence_thresh']),
        args['--transcription_model'], args['--language'])

    src_dir = extract_sources_from_input_paths(input_paths)

    model = load_transcription_model(transcription_model)

    transcribed_clips_by_speaker  = {}

    for root, _, files in walk_src_files(src_dir):
        for file_name in files:
            if file_name.lower().endswith(('.wav', '.mp3', '.flac', '.ogg')):
                speaker = extract_username(file_name, discord_usernames)

                audio = load_audio(root, file_name)
                nonsilent_sections = detect_nonsilent_sections_from_audio(audio, file_name, pause_len, db_silence_thresh)
                audio_clips = create_audio_clips(file_name, nonsilent_sections, audio)
                transcribed_clips = transcribe_audio_clips(audio_clips, model, speaker, pause_len, mode,
                                                           language)

                if speaker not in transcribed_clips_by_speaker:
                    transcribed_clips_by_speaker[speaker] = []

                for (start, end), text, words in transcribed_clips:
                    transcribed_clips_by_speaker[speaker] = merge_transcripts(
                        transcribed_clips_by_speaker[speaker],
                        [[(start, end), speaker, text, words, False, False, []]], pause_len, mode
                    )

    all_transcribed_clips = []
    for speaker, clips in transcribed_clips_by_speaker.items():
        all_transcribed_clips = merge_transcripts(all_transcribed_clips, clips, pause_len, mode)

    if mode == 'embed':
        all_transcribed_clips = embed_interjections(all_transcribed_clips)

    export_transcript(all_transcribed_clips, output_path, mode)


if __name__ == "__main__":
    main()
