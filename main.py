from speech_recognition.long_transcription import transcribe_gcs
import os
import io
import difflib

output_file = 'data/output.txt'
original_file = 'data/original.txt'
diff_file = 'data/diff.txt'

def upload_data_to_gc():
    print('Make sure your audio files are already uploaded to GCP')

def transcribe():
    print('Start transcribing')
    
    io.open(output_file, 'w').close()

    for i in range(35):
        file_name = 'gs://lt-dictation-to-text/sentences/{0}.flac'.format(i)
        print(file_name)
        transcribe_gcs(file_name, i, output_file)

    print('Transcription results written to ' + output_file)
    print('End transcribing')

def compare_source_with_results():
    print('Start comparing')

    io.open(diff_file, 'w').close()

    diff = difflib.ndiff(
        io.open(original_file, encoding="utf-8").readlines(),
        io.open(output_file, encoding="utf-8").readlines())

    with io.open(diff_file, 'w', encoding="utf-8") as out:
        out.write(''.join(diff))

    print('Diff results written to ' + diff_file)
    print('End comparing')

if __name__ == "__main__":
    upload_data_to_gc()
    #transcribe()
    compare_source_with_results()
