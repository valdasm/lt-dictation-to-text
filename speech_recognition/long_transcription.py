import io

def transcribe(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='lt-LT')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    return response

def transcribe_gcs_detailed(gcs_uri, sentence_nr, file_name):
   
    response = transcribe(gcs_uri)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    
    with io.open(file_name, 'a', encoding="utf-8") as out:
        out.write('#{0}\n'.format(sentence_nr))
        for result in response.results:
            out.write('{0}\n'.format(result.alternatives[0].transcript.strip()))
            out.write('{0}\n'.format(result.alternatives[0].confidence))

def transcribe_gcs(gcs_uri, sentence_nr, file_name):
    
    response = transcribe(gcs_uri)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    
    if (not response.results) and  (len(response.result) < 2):
        print('Empty or not complete result set. Expecting at least two transcribed sentences.')
        return

    first_sentence = select_highest_confidence_alternative(response.results[0])
    last_sentence = select_highest_confidence_alternative(response.results[-1])
  
    highest_confidence_sentence = ''
    if (first_sentence[1] > last_sentence[1]):
        highest_confidence_sentence = first_sentence[0]
    else:
        highest_confidence_sentence = last_sentence[0]
    
    with io.open(file_name, 'a', encoding="utf-8") as out:
        out.write('{0}\n'.format(highest_confidence_sentence))

def select_highest_confidence_alternative(result):
    highest_confidence = 0.0
    sentence = ''
    for alt in result.alternatives:
        if alt.confidence > highest_confidence:
            highest_confidence = alt.confidence
            sentence = alt.transcript.strip()

    return (sentence, highest_confidence)
        