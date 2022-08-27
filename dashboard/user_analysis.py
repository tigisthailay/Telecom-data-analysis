#System Modules
import os
import sys
sys.path.append(os.path.abspath(os.path.join('..')))
#sys.path.insert(0, './pages')
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

import script.ploting as plot
#This is User Averview Analysis
st.subheader('overciew page')
st.set_option('deprecation.showPyplotGlobalUse', False)
class OverviewAnalysis:
  def __init__(self, df):
    self.df_overview = df

  def overview_analysis(self):
    st.write("User Overview Analysis")
   
    top_10_handset = self.df_overview.groupby("Handset Type")['MSISDN/Number'].nunique().nlargest(10)
    top_3_manufacturers = self.df_overview.groupby("Handset Manufacturer")['MSISDN/Number'].nunique().nlargest(3)

    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(12,7))
    plot.serious_bar(top_3_manufacturers, ax1)
    plot.serious_bar(top_10_handset, ax2)
    plt.xticks(rotation=75)
    st.pyplot()

    top_manufacturer =self.df_overview.groupby("Handset Manufacturer").agg({"MSISDN/Number":'count'}).reset_index()
    top_3_manufacturers = top_manufacturer.sort_values(by='MSISDN/Number', ascending=False).head(3)
    manufacturers = self.df_overview.groupby("Handset Manufacturer")
    st.write("The top 5 handsets type of the top 3 handset manufacturer are ")

    # Top five Handset Type in the top 3 manufacturing 

    for column in top_3_manufacturers['Handset Manufacturer']:
      result = manufacturers.get_group(column).groupby("Handset Type")['MSISDN/Number'].nunique().nlargest(5)
      st.write(f" the { column } ")
      #print("i am at the overview")
      print(result)
      st.write(result.head())
    st.write(" Overview Analysis outcomes")
