"""
https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries

Synchronous
Transcribed audio files of more than 1 min in duration

"""
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

def transcribe_gcs_detailed(gcs_uri, sentence_nr):
    """Audio file should contain sentence and phrases repetitions. Outputs all transcribed sentences and confidence values"""
    response = transcribe(gcs_uri)
    output = []
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.

    output.append('#{0}\n'.format(sentence_nr))
    for result in response.results:
        output.append('{0}\n'.format(result.alternatives[0].transcript.strip()))
        output.append('{0}\n'.format(result.alternatives[0].confidence))
    
    return output

def transcribe_gcs_single(gcs_uri, sentence_nr):
    """Audio transcribed as single sentence"""
    response = transcribe(gcs_uri)
    sentence = ''
    
    for phrase in response.results:
        alternative = select_highest_confidence_alternative(phrase)
        sentence += alternative[0]

    return ['{0}\n'.format(sentence)]

def transcribe_gcs_repeated(gcs_uri, sentence_nr):
    """Audio file should contain sentence repetitions. Takes first and last, outputs transcription of highest confidence"""
    response = transcribe(gcs_uri)
    output = []
    
    if (not response.results) and  (len(response.result) < 2):
        print('Empty or not complete result set. Expecting at least two transcribed sentences.')
        return

    first_sentence = select_highest_confidence_alternative(response.results[0])
    last_sentence = select_highest_confidence_alternative(response.results[-1])
  
    if (first_sentence[1] > last_sentence[1]):
        output.append('{0}\n'.format(first_sentence[0]))
    else:
        output.append('{0}\n'.format(last_sentence[0]))
    
    return output

def select_highest_confidence_alternative(result):
    highest_confidence = 0.0
    sentence = ''
    for alt in result.alternatives:
        if alt.confidence > highest_confidence:
            highest_confidence = alt.confidence
            sentence = alt.transcript.strip()

    return (sentence, highest_confidence)
        