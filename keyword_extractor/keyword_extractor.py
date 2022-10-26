import gcsfs
import google.cloud.bigquery as bq
import pickle
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
import re

# Not sure if we need these two imports
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from scipy.sparse import coo_matrix

fs = gcsfs.GCSFileSystem(project = 'durable-catbird-204706')

##Creating a list of stop words and adding custom stopwords
stop_words = set(stopwords.words("english"))
##Creating a list of custom stopwords
new_words = ["using", "show", "result", "large", "also", "iv", "one", "two", "new", "previously", "shown"]
stop_words = stop_words.union(new_words)
# Lemmatization
lem = WordNetLemmatizer()


with fs.open('biotech_lee/keyword_extractor/cv.pkl', 'rb') as file:
    cv = pickle.load(file)    


with fs.open('biotech_lee/keyword_extractor/tfidf.pkl', 'rb') as file:
    tfidf_transformer = pickle.load(file)


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    # use only topn items from vector
    sorted_items = sorted_items[:topn]
    score_vals = []
    feature_vals = []
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
    # create a tuples of feature,score
    # results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]
    return results
    
    
def get_keywords_from_question(question, topn=5):
    # Clean question

    text = re.sub('[^a-zA-Z]', ' ', question)
    # Convert to lowercase
    text = text.lower()
    # remove tags
    text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)
    # remove special characters and digits
    text = re.sub("(\\d|\\W)+", " ", text)
    text = re.sub("(\\d|\\W)+", " ", text)
    text = text.split()
    text = set(word for word in text if not word in stop_words)
    text = set(lem.lemmatize(word) for word in text if not word in stop_words)
    text = ' '.join(text)
    # Predict keywords from the question
    feature_names=cv.get_feature_names()
    tf_idf_vector = tfidf_transformer.transform(cv.transform([text]))
    sorted_items = sort_coo(tf_idf_vector.tocoo())
    keywords = extract_topn_from_vector(feature_names, sorted_items, topn)

    return keywords

def get_clean_words(question):
    # Clean question
    text = re.sub('[^a-zA-Z]', ' ', question)
    # Convert to lowercase
    text = text.lower()
    # remove tags
    text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)
    # remove special characters and digits
    text = re.sub("(\\d|\\W)+", " ", text)
    text = text.split()
    text = set(word for word in text if not word in stop_words)
    text = set(lem.lemmatize(word) for word in text if not word in stop_words)
    clean_words = []
    for word in text:
        clean_words.append(word)

    return clean_words