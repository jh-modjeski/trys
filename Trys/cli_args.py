from docopt import docopt


def parse_arguments():
    usage = """
    Usage:
    main.py <input>... [--output=OUTPUT] [--discord] [--experimental] [--transcription_model=TM] [--min_silence_len=MSL] [--silence_thresh=ST]

    Options:
    -o --output=OUTPUT              Output file path [default: transcript.txt]
    -d --discord                    Extract discord username from file names
    -e --experimental               Experimental mode that uses the start and end time of each word
    -m --transcription_model=TM     Transcription model to use (available: tiny, base, small, medium, large) [default: large]
    -l --min_silence_len=MSL        Minimum silence length in milliseconds [default: 1500]
    -t --silence_thresh=ST          Silence threshold in dB [default: -50]
    """

    args = docopt(usage)
    args['username_regex'] = r'^\d+-(.+?)_\d+.*$' if args['--discord'] else None

    return args
