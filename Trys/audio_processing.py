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


def transcribe_audio_clips(audio_clips, model, speaker, min_silence_len, experimental):
    if experimental:
        return transcribe_audio_clips_experimental(audio_clips, model, speaker, min_silence_len)
    else:
        return transcribe_audio_clips_stable(audio_clips, model, speaker)


def transcribe_audio_clips_stable(audio_clips, model, speaker):
    temp_dir = create_clips_dir()
    transcribed_clips = []

    for (start, end), audio_clip in tqdm(audio_clips, desc=f"Transcribing {speaker}", unit="clips"):
        with open(f"{temp_dir}/clips/clip.wav", "wb") as f:
            audio_clip.export(f, format="wav")

            result = model.transcribe(f"{temp_dir}/clips/clip.wav")

            if result["text"]:
                transcribed_clips.append(((start, end), result["text"]))

    return transcribed_clips


def transcribe_audio_clips_experimental(audio_clips, model, speaker, min_silence_len):
    temp_dir = create_clips_dir()
    transcribed_clips = []

    for (start, end), audio_clip in tqdm(audio_clips, desc=f"Transcribing {speaker}", unit="clips"):
        with open(f"{temp_dir}/clips/clip.wav", "wb") as f:
            audio_clip.export(f, format="wav")

            result = model.transcribe(f"{temp_dir}/clips/clip.wav", word_timestamps=True)

            if result["text"]:
                words = result["segments"][0]["words"]
                for segment in result["segments"][1:]:
                    words.extend(segment["words"])

                transcript_start = start
                transcript_text = []
                for i, word in enumerate(words):
                    if i == 0:
                        transcript_text.append(word["word"])
                    else:
                        # Audio may have been detected that could not be transcribed. We should treat these gaps as silence.
                        gap = (word["start"] * 1000) - (words[i - 1]["end"] * 1000)
                        if gap > min_silence_len:
                            transcribed_clips.append(((int(transcript_start), int(start + words[i - 1]["end"] * 1000)),
                                                      " ".join(transcript_text)))
                            transcript_start = start + word["start"] * 1000
                            transcript_text = [word["word"]]
                        else:
                            transcript_text.append(word["word"])

                transcribed_clips.append(((int(transcript_start), int(start + words[-1]["end"] * 1000)),
                                          " ".join(transcript_text)))

    return transcribed_clips