# lt-dictation-to-text

# Data
**data\sentences**

Single file contains single audio sentence whithout repetitions. Used for further comparison analysis.

**data\sentences_repeated**

Here we have dictation, full sentence at the beginning and at the end + phrase repetitions. Not used for further comparison analysis. Transcription and confidence levels can be found in data\raw_detailed_output.md

An example of a single audio file:
* This is a sentence about my city
* This is
* a sentence
* about my city
* This is a sentence about my city

# Setup

* GCP plan required
* gsutil required to move audio files to Google Storage
* python -m venv venv
* venv\Scripts\activate.bat
* pip install -r requirements.txt
* SET GOOGLE_APPLICATION_CREDENTIALS=[PATH_to_google_service_account_json]

# TODO

1. Use sentences_repeated and phrases for better results