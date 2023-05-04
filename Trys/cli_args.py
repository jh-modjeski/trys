from docopt import docopt


def parse_arguments():
    usage = """
    Usage:
    main.py <input>... [--output=OUTPUT] [--discord] [--experimental] [--transcription_model=TM] [--pause_len=PL] [--silence_thresh=ST] [--language=LANG]

    Options:
    -o --output=OUTPUT              Output file path [default: transcript.txt]
    -d --discord                    Extract discord username from file names
    -e --experimental               Experimental mode that uses the start and end time of each word
    -m --transcription_model=TM     Transcription model to use (available: tiny, base, small, medium, large) [default: large]
    -p --pause_len=PL               Minimum silence length in milliseconds before making a new clip [default: 1500]
    -t --silence_thresh=ST          Silence threshold in dB [default: -50]
    -l --language=LANG              Language to use for transcription [default: English]
    """

    return docopt(usage)
