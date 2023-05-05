import re


def extract_username(file_name, discord_usernames):
    pattern = r'^\d+-(.+?)_\d+.*$' if discord_usernames else r'^(.+?)\.[^.]*$'
    return re.search(pattern, file_name).group(1)


def merge_transcripts(transcripts1, transcripts2, pause_len, mode):
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
            if mode == 'tag' or mode == 'embed':
                k = j
                overlap = True
                while overlap is True and k < len(transcripts2):
                    overlap = process_transcripts_for_overlaps(transcripts1[i], transcripts2[k], pause_len, mode)
                    k += 1

            i += 1
        else:
            result.append(transcripts2[j])
            if mode == 'tag' or mode == 'embed':
                k = i
                overlap = True
                while overlap is True and k < len(transcripts1):
                    overlap = process_transcripts_for_overlaps(transcripts2[j], transcripts1[k], pause_len, mode)
                    k += 1

            j += 1

    result.extend(transcripts1[i:])
    result.extend(transcripts2[j:])

    return result


def process_transcripts_for_overlaps(p_transcript, s_transcript, pause_len, mode):
    if p_transcript[3] is True or s_transcript[4] is True:
        # transcript already processed
        return True

    p_start, p_end = p_transcript[0]
    s_start, s_end = s_transcript[0]

    if s_start < p_end:
        if s_end <= p_end:
            if s_end - s_start <= pause_len:
                s_transcript[4] = True
                if mode == 'embed':
                    p_transcript[6].append(s_transcript)
            else:
                s_transcript[5] = True
        elif p_end - s_start > pause_len:
            s_transcript[5] = True

        return True

    return False


def format_timestamp(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def embed_interjections(clips):
    for clip in clips:
        if clip[6]:  # Check if interjections list is not empty
            primary_statement_words = clip[3]
            interjections = clip[6]

            for interjection in interjections:
                interjection_start = interjection[3][0]['t']

                # Find the index of the word where the interjection should be inserted
                insert_index = -1
                for i, word in enumerate(primary_statement_words):
                    if interjection_start < word['t']:
                        insert_index = i
                        break

                # Insert the interjection text and update the words list
                if insert_index != -1:
                    interjection_text = f" ({interjection[1]}: {interjection[2]})"
                    primary_statement_words = (primary_statement_words[:insert_index] +
                                               [{'w': interjection_text, 't': interjection_start}] +
                                               primary_statement_words[insert_index:])
                else:
                    primary_statement_words.append({'w': interjection[2], 't': interjection_start})

            # Update the primary statement text and words list
            clip[2] = "".join([word['w'] for word in primary_statement_words])
            clip[3] = primary_statement_words

    return clips
