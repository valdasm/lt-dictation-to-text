# lt-dictation-to-text

#### Setup

https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries#client-libraries-install-python
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
set GOOGLE_APPLICATION_CREDENTIALS=[PATH_to_google_service_account_json]
set GOOGLE_APPLICATION_CREDENTIALS=C:\asdf
set BUCKET=your_bucket
gsutil -m cp -r data/sentences gs://your_bucket/sentences

#### TODO
(/) 1. Upload files to GS 
2. https://cloud.google.com/speech-to-text/docs/async-recognize