import whisper
from halo import halo
from pydub.silence import detect_nonsilent
from tqdm import tqdm

from Trys.file_management import create_tmp_dir, create_clips_dir


@halo.Halo(text='Loading transcription model', spinner='dots')
def load_transcription_model(transcription_model):
    return whisper.load_model(transcription_model)


@halo.Halo(text='Detecting nonsilent audio', spinner='dots')
def detect_nonsilent_sections_from_audio(audio, file_name, min_silence_len, silence_thresh):
    return detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)


def create_audio_clips(file_name, nonsilent_sections, audio):
    audio_clips = []

    for start, end in tqdm(nonsilent_sections, desc=f"Creating nonsilent audio clips from {file_name}",
                           unit="clips"):
        clip = audio[start:end]
        audio_clips.append(((start, end), clip))

    return audio_clips


def transcribe_audio_clips(audio_clips, model, speaker, min_silence_len, mode, language):
    if mode == 'basic' or mode == 'tag':
        return transcribe_audio_clips_stable(audio_clips, model, speaker, language)
    else:
        return transcribe_audio_clips_experimental(audio_clips, model, speaker, min_silence_len, language)


def transcribe_audio_clips_stable(audio_clips, model, speaker, language):
    temp_dir = create_clips_dir()
    transcribed_clips = []

    for (start, end), audio_clip in tqdm(audio_clips, desc=f"Transcribing {speaker}", unit="clips"):
        with open(f"{temp_dir}/clips/clip.wav", "wb") as f:
            audio_clip.export(f, format="wav")

            result = model.transcribe(f"{temp_dir}/clips/clip.wav", language=language)

            if result["text"]:
                transcribed_clips.append(((start, end), result["text"], []))

    return transcribed_clips


def transcribe_audio_clips_experimental(audio_clips, model, speaker, min_silence_len, language):
    temp_dir = create_clips_dir()
    transcribed_clips = []

    for (start, end), audio_clip in tqdm(audio_clips, desc=f"Transcribing {speaker}", unit="clips"):
        with open(f"{temp_dir}/clips/clip.wav", "wb") as f:
            audio_clip.export(f, format="wav")

            result = model.transcribe(f"{temp_dir}/clips/clip.wav", word_timestamps=True, language=language)

            if result["text"]:
                words = result["segments"][0]["words"]
                for segment in result["segments"][1:]:
                    words.extend(segment["words"])

                words = [{'w': w['word'], 't': start + calculate_word_time_average(w)} for w in words]

                transcript_start = start
                transcript_text = []
                transcript_words = []
                for i, word in enumerate(words):
                    if i == 0:
                        transcript_start = word['t']
                        transcript_text.append(word["w"])
                        transcript_words.append(word)
                    else:
                        # Audio may have been detected that could not be transcribed. Treat these gaps as silence.
                        gap = word['t'] - words[i - 1]['t']
                        if gap > min_silence_len:
                            transcribed_clips.append(((int(transcript_start), int(words[i - 1]['t'])),
                                                      "".join(transcript_text), transcript_words))

                            transcript_start = word['t']
                            transcript_text = [word["w"]]
                            transcript_words = [word]
                        else:
                            transcript_text.append(word["w"])
                            transcript_words.append(word)

                transcribed_clips.append(((int(transcript_start), int(words[-1]['t'])),
                                          "".join(transcript_text), transcript_words))

    return transcribed_clips


def calculate_word_time_average(word):
    # Whisper returns inconsistent results for word start and end time. Averaging the two seems to work well, however.
    return 1000 * (word["start"] + word["end"]) / 2

