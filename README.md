# lt-dictation-to-text

#### Data
**data\sentences**
Single file contains single sentence whithout repetitions

**data\sentences_repeated**
Here we have dictation, full sentence at the beginning and at the end + phrase repetitions. In two files there is a blend between a sentence and repetition. Hence Google picks
An example of a single audio file:
* This is a sentence about my city
* This is
* a sentence
* about my city
* This is a sentence about my city

#### Setup


* gsutil required to move sentences to Google Storage
* python -m venv venv
* venv\Scripts\activate.bat
* pip install -r requirements.txt
* SET GOOGLE_APPLICATION_CREDENTIALS=[PATH_to_google_service_account_json]



#### TODO
(/) 1. Upload files to GS 
(/) 2. https://cloud.google.com/speech-to-text/docs/async-recognize
(/) 3. Split audio into files (sentences without repetitions)