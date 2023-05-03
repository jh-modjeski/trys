# Trys -TRanscrYpt Stitcher

Trys is a powerful audio transcription tool for podcast-style recordings, transcribing multiple audio files and stitching them together into a single transcript. I recommend using [CraigChat](https://github.com/CraigChat/craig) for great recordings on Discord. Trys uses Whisper by OpenAI for automatic speech recognition and provides options for different transcription models, silence detection, and more.

## That's a weird name

Yeah, but it sounds like Triss Merigold - so that's what we're going with. Let's not think too hard about it, or you might notice that there's no Y in transcript either.

## Features

- Supports single or multiple input files in standard audio formats
- Automatically detects and extracts usernames from Discord audio file names
- Experimental mode for precise word-level timestamps
- Adjustable silence detection and minimum silence length
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

## Usage

```main.py <input>... [--output=OUTPUT] [--discord] [--experimental] [--transcription_model=TM] [--min_silence_len=MSL] [--silence_thresh=ST]```

### Options

- `-o --output`: Output file path `[default: transcript.txt]`
- `-d --discord`: Extract Discord username from file names (use this with [CraigChat](https://github.com/CraigChat/craig) or similar tools)
- `-e --experimental`: Experimental mode that uses the start and end time of each word
- `-m --transcription_model`: Transcription model to use (available: tiny, base, small, medium, large) `[default: large]`
- `-l --min_silence_len`: Minimum silence length in milliseconds `[default: 1500]`
- `-t --silence_thresh`: Silence threshold in dB `[default: -50]`

## Examples

To transcribe a single file:

```python main.py audio_file.ogg```


To transcribe multiple files:

```python main.py audio_file_1.ogg audio_file_2.ogg```

To transcribe files in a folder

```python main.py /audio```

To transcribe zipped files:

```python main.py collection.zip```


To transcribe a Discord audio file with username extraction:

```python main.py /input/audio_file1.ogg /input/audio_file2.ogg --discord```


To enable experimental mode with word-level timestamps:

```python main.py /input/audio_file.ogg --experimental```


## Dependencies

Trys requires the following libraries:

- docopt
- halo
- pydub
- tqdm
- whisper

You may need to follow a guide for setting up Whisper from OpenAI, if you're not already setup.
