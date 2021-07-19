import streamlit as st
import traceback
import numpy as np

import time
import matplotlib.pyplot as plt
from star_sweep.crawler import *
from star_sweep.analyzer import *

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
    result = getDataframe(search_input, int(num_articles))
    print(len(result))
except Exception as e:
    print(e)

st.write(len(result))
st.dataframe(result)
print(result)
