import streamlit as st
import traceback
import numpy as np
import time
import matplotlib.pyplot as plt
from star_sweep.crawler import *

# from sklearn import datasets
# from sklearn.model_selection import train_test_split
# from sklearn.decomposition import PCA
# from sklearn.svm import SVC
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score

st.title("""Star Sweep version 1.0""")

st.write(
    """
## Test
"""
)


search_input = st.sidebar.text_input("Finding Topic")
num_articles = st.sidebar.text_input("Amout of articles (sort by latest)")
st.write(f"## {search_input} ")
result = []
try:
    result = getArticle(search_input, int(num_articles))
    print(len(result))
except:
    pass

st.write(len(result))
