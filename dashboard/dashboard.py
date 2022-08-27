import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
from insert_data  import db_execute_fetch

st.set_page_config(page_title="Day 5", layout="wide")

def loadData():
    query = "select * from TelecomDataTable"
    df = db_execute_fetch(query, dbName="Telecom-DB", rdf=True)
    return df

def selectHashTag():
    df = loadData()
    hashTags = st.multiselect("choose combaniation of hashtags", list(df['hashtags'].unique()))
    if hashTags:
        df = df[np.isin(df, hashTags).any(axis=1)]
        st.write(df)

def selectLocAndAuth():
    df = loadData()
    location = st.multiselect("choose Location of tweets", list(df['place'].unique()))
    lang = st.multiselect("choose Language of tweets", list(df['language'].unique()))

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
