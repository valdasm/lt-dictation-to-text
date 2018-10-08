from speech_recognition.long_transcription import transcribe_gcs_single, transcribe_gcs_detailed, transcribe_gcs_repeated
from text_analysis import wer
import os
import io
import difflib
import re, string
# from itertools import zip

original_file = 'data/raw_original.txt'
original_cleaned_file = 'data/cleaned_original.txt'

google_output_file = 'data/google/raw_output.txt'
google_output_cleaned_file = 'data/google/cleaned_output.txt'
google_output_detailed_file = 'data/google/raw_detailed_output.md'
google_diff_file = 'data/google/diff.txt'
gs_repeated_audio_path = 'gs://lt-dictation-to-text/sentences_repeated/{0}.flac'
gs_audio_path = 'gs://lt-dictation-to-text/sentences/{0}.flac'

tilde_output_file = 'data/tilde/raw_output.txt'
tilde_output_cleaned_file = 'data/tilde/cleaned_output.txt'
tilde_diff_file = 'data/tilde/diff.txt'

def setup_google():
    print('##### SET PATH TO GOOGLE SERVICE USER JSON FILE #####')
    print('SET GOOGLE_APPLICATION_CREDENTIALS=[PATH_to_google_service_account_json]\n')
    print('#####      UPLOAD FILES TO GOOGLE STORAGE       #####')
    print('gsutil -m cp -r data/sentences_repeated gs://your_bucket/sentences_repeated\n')
    print('gsutil -m cp -r data/sentences gs://your_bucket/sentences\n')

def setup_tilde():
    print('##### https://www.tilde.lt/snekos-technologijos #####')
    print('##### Upload manually and receive results via email #####')
    

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

def compare_files(file1, file2, result_file):
    print('* Start comparison using difflib')

    io.open(result_file, 'w').close()

    diff = difflib.ndiff(
        io.open(file1, encoding="utf-8").readlines(),
        io.open(file2, encoding="utf-8").readlines())

    with io.open(result_file, 'w', encoding="utf-8") as out:
        out.write(''.join(diff))

    print('Diff results written to ' + result_file)
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

def run_google_speech_recognition():

    setup_google()

    contexts = [
        # Single sentence transcription 
        #(transcribe_gcs_single, google_output_file, gs_audio_path, 35),

        # Two times repeated sentence transcription 
        (transcribe_gcs_repeated, google_output_file, gs_repeated_audio_path, 35),

        # Repeated sentences and phrases transcription + confidences; NOT USED in further analysis
        (transcribe_gcs_detailed, google_output_detailed_file, gs_repeated_audio_path, 35)
        ]
   
    # clean original file
    clean_files_for_word_analysis(original_file, original_cleaned_file)

    # Detailed transcription on repeated phrases (INDEX 1) IS NOT used in further analysis. Just scoring phases and saving to a file
    for i in range(len(contexts)): #range(0,2)
       transcribe(contexts[i][0], contexts[i][1], contexts[i][2], contexts[i][3]) 
     
    clean_files_for_word_analysis(google_output_file, google_output_cleaned_file)
    compare_files(original_cleaned_file, google_output_cleaned_file, google_diff_file)
    evaluate_transcription(google_output_cleaned_file, original_cleaned_file)

def run_tilde_speech_recognition():
    setup_tilde()

    # Cleaning files from punctation marks
    clean_files_for_word_analysis(tilde_output_file, tilde_output_cleaned_file)
    compare_files(original_cleaned_file, tilde_output_cleaned_file, tilde_diff_file)
    evaluate_transcription(tilde_output_cleaned_file, original_cleaned_file)
   
    # compare_files(original_file, tilde_output_file, tilde_diff_file)
    # evaluate_transcription(tilde_output_file, original_file)

if __name__ == "__main__":

    # run_google_speech_recognition()
    run_tilde_speech_recognition()

    


