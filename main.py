from speech_recognition.long_transcription import transcribe_gcs_single, transcribe_gcs_detailed, transcribe_gcs_repeated
from text_analysis import wer
import os
import io
import difflib
import re, string
# from itertools import zip

output_file = 'data/raw_output.txt'
output_cleaned_file = 'data/cleaned_output.txt'
output_detailed_file = 'data/raw_detailed_output.md'
original_file = 'data/raw_original.txt'
original_cleaned_file = 'data/cleaned_original.txt'
diff_file = 'data/diff.txt'
gs_repeated_audio_path = 'gs://lt-dictation-to-text/sentences_repeated/{0}.flac'
gs_audio_path = 'gs://lt-dictation-to-text/sentences/{0}.flac'

def setup():
    print('##### SET PATH TO GOOGLE SERVICE USER JSON FILE #####')
    print('SET GOOGLE_APPLICATION_CREDENTIALS=[PATH_to_google_service_account_json]\n')
    print('#####      UPLOAD FILES TO GOOGLE STORAGE       #####')
    print('gsutil -m cp -r data/sentences_repeated gs://your_bucket/sentences_repeated\n')
    print('gsutil -m cp -r data/sentences gs://your_bucket/sentences\n')

def transcribe(transcription_function, results_file_name, gs_path, audio_files_count):
    print('* Start transcription')
    print('Transcription function ' + transcription_function.__name__)
    
    output_lines = []
    for i in range(audio_files_count):
        audio_file_path = gs_path.format(i)
        print(audio_file_path)
        output_lines.extend(transcription_function(audio_file_path, i))

    with io.open(results_file_name, 'w', encoding="utf-8") as out:
        for line in output_lines:
            out.write(line)

    print('Transcription results written to ' + results_file_name)
    print('* End transcription')

def compare_files(file1, file2):
    print('* Start comparison using difflib')

    io.open(diff_file, 'w').close()

    diff = difflib.ndiff(
        io.open(file1, encoding="utf-8").readlines(),
        io.open(file2, encoding="utf-8").readlines())

    with io.open(diff_file, 'w', encoding="utf-8") as out:
        out.write(''.join(diff))

    print('Diff results written to ' + diff_file)
    print('* End comparison')

def clean_files_for_word_analysis(raw_file, cleaned_file):
    print('* Start cleaning')
    print('Strip everything but spaces and alphanumeric')
    with io.open(raw_file, 'r', encoding="utf-8") as file_input,\
        io.open(cleaned_file, 'w', encoding="utf-8") as file_output:
        for line in file_input:
            line = line.rstrip().lower()
            pattern = re.compile('([^\s\w]|_)+')
            output_line = ''.join(pattern.sub('', line))
            file_output.write(output_line + '\n')
    print('Cleaned file ' + cleaned_file)
    print('* End cleaning')


def evaluate_transcription(outputted_file, reference_file):
    """https://en.wikipedia.org/wiki/Word_error_rate"""
    print('* Start evaluation')

    wer.execute_wer(outputted_file, reference_file)

    print('* End evaluation')

if __name__ == "__main__":

    #transcription function, output_file, google storage path, files to process

    contexts = [
        # Single sentence transcription 
        #(transcribe_gcs_single, output_file, gs_audio_path, 35),

        # Two times repeated sentence transcription 
        (transcribe_gcs_repeated, output_file, gs_repeated_audio_path, 35)

        # Repeated sentences and phrases transcription + confidences; NOT USED in further analysis
        #(transcribe_gcs_detailed, output_detailed_file, gs_repeated_audio_path, 35)
        ]

    setup()
    
    # clean original file
    clean_files_for_word_analysis(original_file, original_cleaned_file)

    # Detailed transcription on repeated phrases (INDEX 1) IS NOT used in further analysis. Just scoring phases and saving to a file
    for i in range(len(contexts)): #range(0,2)
       transcribe(contexts[i][0], contexts[i][1], contexts[i][2], contexts[i][3]) 
     
    clean_files_for_word_analysis(output_file, output_cleaned_file)
    compare_files(original_cleaned_file, output_cleaned_file)
    evaluate_transcription(output_cleaned_file, original_cleaned_file)
