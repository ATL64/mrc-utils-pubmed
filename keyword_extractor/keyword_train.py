#from gcloud import storage
import google.cloud.bigquery as bq
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import HashingVectorizer
import joblib
import pandas as pd
from google.oauth2 import service_account
import pandas_gbq
import pickle

credentials_path = "/home/creds.json"
#client = bq.Client.from_service_account_json("/home/creds.json")

credentials = service_account.Credentials.from_service_account_file(
    credentials_path,
)

pandas_gbq.context.credentials = credentials
pandas_gbq.context.project = "xxxx"


query = """
    SELECT distinct abstract
    FROM `pubmed.fact_abstracts`
    WHERE abstract is not null
    limit 1000000
"""


# 4 million takes 15 mins for bq
abstracts_df = pandas_gbq.read_gbq(query,
                                   project_id="xxxx",
                                   credentials=credentials,
                                   dialect='standard',
                                   configuration={'query': {"allow_large_results":True}}
                                   )


abstract_list = abstracts_df['abstract'].tolist()


print('finish table download')

#A few seconds
abstracts = []
for s in abstract_list:
    abst = s.replace("\n", '')
    a = abst.find('abstract')
    abst = abst[(a + 10):len(abst)]
    b = abst.find('"')
    abst = abst[0:b]
    abstracts.append(s)

del abstract_list

##Creating a list of stop words and adding custom stopwords
stop_words = set(stopwords.words("english"))
##Creating a list of custom stopwords
new_words = ["using", "show", "result", "large", "also", "iv", "one", "two", "new", "previously", "shown"]
stop_words = stop_words.union(new_words)

# For 1 million abstracts, this takes around 14 minutes
# 4 million abstracts, 43 minutes
corpus = []
for i in range(0, len(abstracts)):
    # Remove punctuations
    text = re.sub('[^a-zA-Z]', ' ', abstracts[i])
    # Convert to lowercase
    text = text.lower()
    # remove tags
    text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)
    # remove special characters and digits
    text = re.sub("(\\d|\\W)+", " ", text)
    ##Convert to list from string
    text = text.split()
    ##Stemming
    ps = PorterStemmer()
    # Lemmatisation
    lem = WordNetLemmatizer()
    text = [lem.lemmatize(word) for word in text if not word in stop_words]
    text = " ".join(text)
    corpus.append(text)

print('finish corpus')
len(corpus)

del abstracts

# 1 million rows 50k vector, 1 ngram --> 1 minute
# 4 million rows 200k vector, 1-3 ngram--> Takes a bit more than 1 hour
cv = CountVectorizer(max_df=0.8, stop_words=stop_words, max_features=50000, ngram_range=(1, 1))
# cv=HashingVectorizer(stop_words=stop_words, ngram_range=(1,3))
X = cv.fit_transform(corpus)

print('finish fit_transform')

tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf_transformer.fit(X)

print('finish final fit')


### SAVE TO DISK

# save your model in disk
joblib.dump(tfidf_transformer, 'tfidf.gz')
# 4 million rows 50 minutes
# 1 million, 50k, 1-ngram, a few seconds
joblib.dump(cv, 'cv.gz')


# get feature names
feature_names=cv.get_feature_names()

# write the with pickle
with open('tfidf.pkl', 'wb') as f:
    pickle.dump(tfidf_transformer, f)
#4 million rows: 10:19 --> 10:30
with open('cv.pkl', 'wb') as f:
    pickle.dump(cv, f)

# If you want to check memory usage:
def getCurrentMemoryUsage():
    ''' Memory usage in kB '''
    with open('/proc/self/status') as f:
        memusage = f.read().split('VmRSS:')[1].split('\n')[0][:-3]
    return int(memusage.strip())

