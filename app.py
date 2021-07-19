import streamlit as st
import traceback
import numpy as np
import math
import time
import matplotlib.pyplot as plt
from star_sweep.crawler import *
from star_sweep.analyzer import *
from collections import Counter
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from nltk import flatten
from wordcloud import WordCloud

st.title("""Star Sweep version 0.1""")


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
    df["keywords"] = df["keywords"].apply(lambda x: cleanText(x))
    keywords_count = Counter(flatten(df["keywords"].tolist()))
    most_keywords = [
        key
        for key in keywords_count.keys()
        if keywords_count[key] > round(math.log(len(df), 8))
    ]
    mkw2idx = dict(zip(most_keywords, range(len(most_keywords))))
    df["cat_features"] = df["keywords"].apply(lambda x: createCatArray(x, mkw2idx))
    st.dataframe(df)

    pca_components = 2
    pca = PCA(n_components=pca_components)
    principalComponents = pca.fit_transform(df.cat_features.tolist())
    principalDf = pd.DataFrame(
        data=principalComponents, columns=list(range(pca_components))
    )

    # data_points = [(e[0], e[1]) for e in principalDf]
    x = np.array(principalDf[0].tolist())
    x = (x - x.min()) / (x.max() - x.min())
    y = np.array(principalDf[1].tolist())
    y = (y - y.min()) / (y.max() - y.min())

    fig, ax = plt.subplots()
    ax.scatter(x, y, marker=".")
    st.dataframe(principalDf)
    st.write(len(principalDf))
    st.pyplot(fig)

    clustering = DBSCAN(eps=0.05, min_samples=round(len(df) ** 0.33)).fit(
        list(zip(x, y))
    )

    fig2, ax2 = plt.subplots()
    ax2.scatter(x, y, c=clustering.labels_, marker="*", s=5)
    df["label"] = clustering.labels_
    st.write(len(set(clustering.labels_)))

    st.pyplot(fig2)
    st.dataframe(df)

    df = df[df["label"] != -1]

    for name, group in df.groupby("label"):
        st.markdown(f"topic: {name} amount:{len(group)}")
        text = " ".join(flatten(group.keywords.tolist()))
        wc = WordCloud(width=800, height=400).generate(text)
        st.image(wc.to_array())
