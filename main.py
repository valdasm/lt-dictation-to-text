from speech_recognition.long_transcription import transcribe_gcs, transcribe_gcs_detailed
import os
import io
import difflib

output_file = 'data/output.txt'
output_detailed_file = 'data/output_detailed.md'
original_file = 'data/original.txt'
diff_file = 'data/diff.txt'
gs_files = 'gs://lt-dictation-to-text/sentences/{0}.flac'
audio_files_count = 35

def setup():
    print('##### SET PATH TO GOOGLE SERVICE USER JSON FILE #####')
    print('SET GOOGLE_APPLICATION_CREDENTIALS=[PATH_to_google_service_account_json]\n')
    print('#####      UPLOAD FILES TO GOOGLE STORAGE       #####')
    print('gsutil -m cp -r data/sentences gs://your_bucket/sentences\n')

def transcribe(transcription_function, results_file_name):
    print('Start transcribing')
    print('Transcription function ' + transcription_function.__name__)
    
    io.open(results_file_name, 'w').close()

    for i in range(audio_files_count):
        file_name = gs_files.format(i)
        print(file_name)
        transcription_function(file_name, i, results_file_name)

    print('Transcription results written to ' + results_file_name)
    print('End transcribing')

def compare_original_with_transcribed():
    print('Start comparing')

    io.open(diff_file, 'w').close()

    diff = difflib.ndiff(
        io.open(original_file, encoding="utf-8").readlines(),
        io.open(output_file, encoding="utf-8").readlines())

    with io.open(diff_file, 'w', encoding="utf-8") as out:
        out.write(''.join(diff))

    print('Diff results written to ' + diff_file)
    print('End comparing')

def clean_source_for_detailed_analysis():
    print('Start cleaning source file')
    print('End cleaning source file')
    #clean original file to focus only on words (no whitespaces and no extra symbols)
    #words written correctly
    #words misspelled
    #without lower-upper case

def create_word_level_statistics():
    print('Start creating statistics')
    print('End creating statistics')

if __name__ == "__main__":
    setup()
    # transcribe(transcribe_gcs, output_file)
    # transcribe(transcribe_gcs_detailed, output_detailed_file) 
    # compare_original_with_transcribed()
    clean_source_for_detailed_analysis()
    create_word_level_statistics()
