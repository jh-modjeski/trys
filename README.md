# Trys -TRanscrYpt Stitcher

Trys is a powerful audio transcription tool for podcast-style recordings, transcribing multiple audio files and stitching them together into a single transcript. Each line in the transcript represents a continuous audible section when the speaker was never quiet for longer than a configurable pause_len. I recommend using [CraigChat](https://github.com/CraigChat/craig) for great recordings on Discord. Trys uses Whisper by OpenAI for automatic speech recognition and provides options for different transcription models, silence detection, and more.

## That's a weird name

Yeah, but it sounds like Triss Merigold - so that's what we're going with. Let's not think too hard about it, or you might notice that there's no Y in transcript either.

## Features

- Supports single or multiple input files in standard audio formats (wav, mp3, flac, ogg)
- Automatically detects and extracts usernames from Discord audio file names
- Experimental mode for precise word-level timestamps and embedded interjections.
- Adjustable silence detection and pause length
- Customizable transcription models (tiny, base, small, medium, large)

## Example Output ([Lex Fridman podcast with Andrej Karpathy](https://www.youtube.com/watch?v=oHWuv1Aqrzk))

```
00:00:03.066 - 00:00:12.970 (Lex Fridman):  Is there cool small projects like Archive Sanity and so on that you're thinking about that the world, the ML world can anticipate?
00:00:13.911 - 00:00:25.571 (Andrej Karpathy):  There's always some fun side projects. Archive Sanity is one. Basically, there's way too many archive papers. How can I organize it and recommend papers and so on? I transcribed all of your podcasts.
00:00:25.609 - 00:00:39.749 (Lex Fridman):  What did you learn from that experience? From transcribing the process of, like you like consuming audio books and podcasts and so on. And here's a process that achieves closer to human level performance on annotation.
00:00:40.039 - 00:01:20.665 (Andrej Karpathy):  Yeah, well, I definitely was surprised that transcription with OpenAI's Whisper was working so well compared to what I'm familiar with from Siri and a few other systems, I guess. It works so well, and that's what gave me some energy to try it out, and I thought it could be fun to run on podcasts. It's kind of not obvious to me why Whisper is so much better compared to anything else, because I feel like there should be a lot of incentive for a lot of companies to produce transcription systems, and that they've done so over a long time. Whisper is not a super exotic model. It's a transformer. It takes MEL spectrograms and just outputs tokens of text. It's not crazy. The model and everything has been around for a long time. I'm not actually 100% sure why this.
00:01:20.667 - 00:02:25.555 (Lex Fridman):  It's not obvious to me either. It makes me feel like I'm missing something. Yeah, because there is a huge, even at Google and so on, YouTube transcription. Yeah, it's unclear, but some of it is also integrating into a bigger system. That, so the user interface, how it's deployed and all that kind of stuff. Maybe running it as an independent thing is much easier, like an order of magnitude easier than deploying to a large integrated system like YouTube transcription or anything like meetings. Like Zoom has transcription. That's kind of crappy, but creating an interface where it detects the different individual speakers, it's able to display it in compelling ways, run it in real time, all that kind of stuff. Maybe that's difficult. But that's the only explanation I have because I'm currently paying quite a bit for human transcription, human caption, annotation. And it seems like there's a huge incentive to automate that. It's very confusing.
00:01:24.822 - 00:01:25.697 (Andrej Karpathy):  I'm missing something.
00:01:31.181 - 00:01:31.318 (Andrej Karpathy):  Yeah.
00:02:18.987 - 00:02:19.102 (Andrej Karpathy):  Right.
00:02:24.665 - 00:02:29.533 (Andrej Karpathy):  Yeah. And I think, I mean, I don't know if you looked at some of the whisper transcripts, but they're quite good.
00:02:29.837 - 00:02:52.198 (Lex Fridman):  They're good, and especially in tricky cases. I've seen Whisper's performance on super tricky cases, and it does incredibly well. So I don't know. A podcast is pretty simple. It's high-quality audio, and you're speaking usually pretty clearly. So I don't know. I don't know what OpenAI's plans are either.
00:02:32.797 - 00:02:32.997 (Andrej Karpathy):  Yeah.
00:02:47.045 - 00:02:47.187 (Andrej Karpathy):  Yeah.
00:02:51.711 - 00:03:19.752 (Andrej Karpathy):  Yeah, but there's always like fun projects basically. And stable diffusion also is opening up a huge amount of experimentation, I would say in the visual realm and generating images and videos and movies. And so that's going to be pretty crazy. That's going to almost certainly work and it's going to be really interesting when the cost of content creation is going to fall to zero. You used to need a painter for a few months to paint a thing, and now it's going to be speak to your phone to get your video.
00:03:03.151 - 00:03:04.298 (Lex Fridman):  Yeah, videos now.
00:03:19.970 - 00:03:32.599 (Lex Fridman):  So Hollywood will start using that to generate scenes, which completely opens up, yeah, so you can make a movie like Avatar, eventually, for under a million dollars.
00:03:33.134 - 00:03:37.916 (Andrej Karpathy):  much less maybe just by talking to your phone. I mean, I know it sounds kind of crazy.
```

Here is the same podcast in embed mode.

```
00:00:03.136 - 00:00:12.576 (Lex Fridman):  Is there cool small projects like Archive Sanity and so on that you're thinking about that the world, the ML world can anticipate?
00:00:13.981 - 00:00:24.841 (Andrej Karpathy):  There's always some fun side projects. Archive Sanity is one. Basically, there's way too many archive papers. How can I organize it and recommend papers and so on? I transcribed all of your podcasts.
00:00:25.679 - 00:00:39.319 (Lex Fridman):  What did you learn from that experience? From transcribing the process of, like you like consuming audio books and podcasts and so on. And here's a process that achieves closer to human level performance on annotation.
00:00:40.109 - 00:01:20.639 (Andrej Karpathy):  Yeah, well, I definitely was surprised that transcription with OpenAI's Whisper was working so well compared to what I'm familiar with from Siri and a few other systems, I guess. It works so well, and that's what gave me some energy to try it out, and I thought it could be fun to run on podcasts. It's kind of not obvious to me why Whisper is so much better compared to anything else, because I feel like there should be a lot of incentive for a lot of companies to produce transcription systems, and that they've done so over a long time. Whisper is not a super exotic model. It's a transformer. It takes MEL spectrograms and just outputs tokens of text. It's not crazy. The model and everything has been around for a long time. I'm not actually 100% sure why this is.
00:01:20.867 - 00:01:30.207 (Lex Fridman):  It's not obvious to me either. It makes me feel like I'm missing something. (Andrej Karpathy:  I'm missing something.) Yeah, because there is a huge, even at Google and so on, YouTube transcription.
00:01:31.231 - 00:01:31.231 (Andrej Karpathy):  Yeah.
00:01:31.957 - 00:01:35.647 (Lex Fridman):  Yeah, it's unclear, but some of it is also integrating into a bigger system.
00:01:36.609 - 00:01:36.609 (Andrej Karpathy):  Yeah.
00:01:37.567 - 00:01:53.837 (Lex Fridman):  That, so the user interface, how it's deployed and all that kind of stuff. Maybe running it as an independent thing is much easier, like an order of magnitude easier than deploying to a large integrated system like YouTube transcription or anything like meetings. Like Zoom has transcription.
00:01:55.507 - 00:02:25.397 (Lex Fridman):  That's kind of crappy, but creating a interface where it detects the different individual speakers, it's able to display it in compelling ways, run it in real time, all that kind of stuff. Maybe that's difficult. But that's the only explanation I have because I'm currently paying quite a bit for human transcription, human caption, (Andrej Karpathy:  Right.) annotation. And it seems like there's a huge incentive to automate that. It's very confusing.
00:02:25.395 - 00:02:29.415 (Andrej Karpathy):  Yeah. And I think, I mean, I don't know if you looked at some of the whisper transcripts, but they're quite good.
00:02:29.867 - 00:02:51.817 (Lex Fridman):  They're good, and especially in tricky cases. (Andrej Karpathy:  Yeah.) I've seen Whisper's performance on super tricky cases, and it does incredibly well. So I don't know. A podcast is pretty simple. It's high-quality audio, and you're speaking usually pretty clearly. (Andrej Karpathy:  Yeah.) So I don't know. I don't know what OpenAI's plans are either.
00:02:52.191 - 00:03:18.911 (Andrej Karpathy):  Yeah, but there's always like fun projects basically. And stable diffusion also is opening up a huge amount of experimentation, I would say in the visual realm and generating images and videos and movies. (Lex Fridman:  Yeah, videos now.) And so that's going to be pretty crazy. That's going to almost certainly work and it's going to be really interesting when the cost of content creation is going to fall to zero. You used to need a painter for a few months to paint a thing, and now it's going to be speak to your phone to get your video.
00:03:20.030 - 00:03:22.190 (Lex Fridman):  So Hollywood will start using that to generate scenes,
00:03:24.820 - 00:03:32.270 (Lex Fridman):  which completely opens up, yeah, so you can make a movie like Avatar, eventually, for under a million dollars.
00:03:33.224 - 00:03:36.524 (Andrej Karpathy):  much less maybe just by talking to your phone. I mean, I know it sounds kind of crazy.
```

## Usage

```
    Usage:
        main.py [basic | experimental | tag | embed] <input>... [--output=OUTPUT] [--discord_usernames] [--transcription_model=TM] [--pause_len=PL] [--db_silence_thresh=DST] [--language=LANG]

    Commands:
        basic        Basic mode (default behavior)
        experimental Use experimental features (word_timestamps)
        tag          Tag interjections and crosstalk
        embed        Use experimental features to embed interjections and tag crosstalk (combined mode)

    Options:
        -o --output=OUTPUT              Output file path [default: transcript.txt]
        -u --discord_usernames          Extract discord username from file names
        -m --transcription_model=TM     Transcription model to use (available: tiny, base, small, medium, large) [default: large]
        -p --pause_len=PL               Minimum silence length in milliseconds before making a new clip [default: 1500]
        -d --db_silence_thresh=DST      Silence threshold in dB [default: -50]
        -l --language=LANG              Language to use for transcription [default: English]
```

## Examples

To transcribe a single file:

```python main.py podcast.wav```


To transcribe multiple files:

```python main.py "Lex Fridman.wav" "Andrej Karpathy.wav"```

To transcribe files in a folder

```python main.py /podcast```

To transcribe zipped files:

```python main.py podcast_recordings.zip```


To transcribe a Discord audio file with username extraction:

```python main.py 1-lexf-3812.ogg 2-andrewK-8442.ogg --discord_usernames```


To enable experimental mode with word-level timestamps:

```python main.py experimental /podcast```

To enable tag mode with interjection and crosstalk tagging:

```python main.py tag /podcast```

To enable embed mode with experimental embedded interjections and crosstalk tagging features:

```python main.py embed /podcast```


## Dependencies

Trys was developed with Python3.10 and requires the following libraries:

- docopt
- halo
- pydub
- tqdm
- whisper

You may need to follow a guide for setting up Whisper from OpenAI, if you're not already setup.
