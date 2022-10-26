#!/bin/sh

# This setup works for both training and using just the module
sudo su
cd ..
yes Y | apt-get update
yes Y | apt-get upgrade
yes Y | apt-get install git
yes Y | apt-get install wget
yes Y | apt install python-pip

yes Y | apt install python3-dev python3-pip python3-venv

curl https://sdk.cloud.google.com | bash # This will need "enter" for standard directory and then y/N for helping google and Y for enabling path variable and enter again (so needs piping)
exec -l $SHELL

gcloud init # Choose the service account credentials option nr 1, then specify project_id = xxxx


python3 -m venv --system-site-packages ./venv
source ./venv/bin/activate
pip install --upgrade pip
pip install --upgrade google-cloud-bigquery
pip install nltk
pip install sklearn
pip install joblib
pip install pandas
pip install pandas-gbq
pip install gcloud
pip install gcsfs



nano creds.json

# paste the following

{
  "type": "service_account",
  "project_id": "xxx",
  "private_key_id": "xxxx",
  "private_key": "xxxx",
......
}

### save the file and quit nano (ctrl X -> Y -> enter)

# exit and save

export GOOGLE_APPLICATION_CREDENTIALS=/home/creds.json

# Run the code in keyword_train.py, it will save two files to the current directory

gsutil cp tfidf.gz gs://biotech_lee/keyword_extractor/tfidf.gz

gsutil cp cv.gz gs://biotech_lee/keyword_extractor/cv.gz

gsutil cp tfidf.pkl gs://biotech_lee/keyword_extractor/tfidf.pkl

gsutil cp cv.pkl gs://biotech_lee/keyword_extractor/cv.pkl

#If you get permission denied to write to storage, you can manually authenticate with:

gcloud auth login

# Follow the link and paste in terminal and you are authenticated to upload to storage
