import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
from pushed_data  import db_execute_fetch

st.set_page_config(page_title="Telecom user analysis", layout="wide")

def loadData():
    query = "select * from TeleTable"
    df = db_execute_fetch(query, dbName="Telecom-DB", rdf=True)
    return df


def selectLocAndAuth():
    df = loadData()
    location = st.multiselect("choose Location", list(df['place'].unique()))
    lang = st.multiselect("choose Language ", list(df['language'].unique()))

    if location and not lang:
        df = df[np.isin(df, location).any(axis=1)]
        st.write(df)
    elif lang and not location:
        df = df[np.isin(df, lang).any(axis=1)]
        st.write(df)
    elif lang and location:
        location.extend(lang)
        df = df[np.isin(df, location).any(axis=1)]
        st.write(df)
    else:
        st.write(df)
