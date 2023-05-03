import re


def extract_username(file_name, discord_usernames):
    pattern = r'^\d+-(.+?)_\d+.*$' if discord_usernames else r'^(.+?)\.[^.]*$'
    return re.search(pattern, file_name).group(1)


def merge_transcripts(transcripts1, transcripts2):
    if len(transcripts1) == 0:
        return transcripts2
    elif len(transcripts2) == 0:
        return transcripts1

    result = []
    i, j = 0, 0

    while i < len(transcripts1) and j < len(transcripts2):
        start1, _ = transcripts1[i][0]
        start2, _ = transcripts2[j][0]

        if start1 < start2:
            result.append(transcripts1[i])
            i += 1
        else:
            result.append(transcripts2[j])
            j += 1

    result.extend(transcripts1[i:])
    result.extend(transcripts2[j:])

    return result


def format_timestamp(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
