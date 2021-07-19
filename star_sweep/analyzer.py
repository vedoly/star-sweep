import re
import nltk

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
stopwords = nltk.corpus.stopwords.words("english")


def cleanText(text):
    # text = " ".join(text)
    text = [e.lower() for e in text]
    text = [re.sub("[^-9A-Za-z ]", "", e) for e in text]

    text = [nltk.PorterStemmer().stem(word) for word in text]
    text = [nltk.WordNetLemmatizer().lemmatize(word) for word in text]
    return text


def createCatArray(arr, mkw2idx):

    out = np.zeros((len(mkw2idx)), dtype=int)
    for e in arr:
        if e in mkw2idx:
            out[mkw2idx[e]] = 1
    return out
