from docopt import docopt


def parse_arguments():
    usage = """
    Usage:
        main.py [basic | experimental | tag | embed] <input>... [--output=OUTPUT] [--discord_usernames] [--transcription_model=TM] [--pause_len=PL] [--db_silence_thresh=DST] [--language=LANG]

    Commands:
        basic        Basic mode (default behavior)
        experimental Use experimental features (word_timestamps)
        tag          Tag interjections and crosstalk
        embed        Use experimental features and tag interjections and crosstalk (combined mode)

    Options:
        -o --output=OUTPUT              Output file path [default: transcript.txt]
        -u --discord_usernames          Extract discord username from file names
        -m --transcription_model=TM     Transcription model to use (available: tiny, base, small, medium, large) [default: large]
        -p --pause_len=PL               Minimum silence length in milliseconds before making a new clip [default: 1500]
        -d --db_silence_thresh=DST      Silence threshold in dB [default: -50]
        -l --language=LANG              Language to use for transcription [default: English]
    """

    return docopt(usage)


def get_mode(args):
    basic = args['basic']
    experimental = args['experimental']
    tag = args['tag']
    embed = args['embed']

    # exit if multiple modes are selected
    if sum([basic, experimental, tag, embed]) > 1:
        print('Error: Multiple modes selected')
        exit(1)

    # return mode
    if basic:
        return 'basic'
    elif experimental:
        return 'experimental'
    elif tag:
        return 'tag'
    elif embed:
        return 'embed'
    else:
        return 'basic'

