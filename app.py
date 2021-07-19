import streamlit as st
import traceback
import numpy as np
import math
import time
import matplotlib.pyplot as plt
from star_sweep.crawler import *
from star_sweep.analyzer import *
from collections import Counter


from nltk import flatten

st.title("""Star Sweep version 1.0""")


search_input = st.sidebar.text_input("Finding Topic")
num_articles = st.sidebar.text_input("Amout of articles (sort by latest)")
st.write(f"Topic: {search_input}, Num: {num_articles}")
df = pd.DataFrame()
try:
    df = getDataframe(search_input, int(num_articles))
    print(len(df))
except Exception as e:
    print(e)

st.write(len(df))
st.dataframe(df)
# print(result)
if len(df) > 0:
    df = df.dropna()
    print("x")
    keywords_count = Counter(flatten(df["keywords"].tolist()))
    most_keywords = [
        key
        for key in keywords_count.keys()
        if keywords_count[key] > math.round(math.log(len(df), 8))
    ]
    mkw2idx = dict(zip(most_keywords, range(len(most_keywords))))
    df["keywords"] = df["keywords"].apply(lambda x: cleanText(x))
    df["cat_features"] = df["keywords"].apply(lambda x: createCatArray(x, mkw2idx))
    # st.dataframe(df)

    pca_components = 2


# pca = PCA(n_components=pca_components)
# principalComponents = pca.fit_transform(X)
# principalDf = pd.DataFrame(
#     data=principalComponents, columns=list(range(pca_components))
# )
