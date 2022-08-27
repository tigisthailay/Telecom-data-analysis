import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

import script.ploting as plot
import script.utils as utils
#This Code is for engaement analysis
st.set_option('deprecation.showPyplotGlobalUse', False)

def get_user_related_columns(df):

  aggrigate = {
      'Total Social Media':'sum',
      'Total Google': 'sum', 
      'Total Youtube': 'sum', 
      'Total Netflix':'sum',
      'Total Gaming':'sum',
      'Total Other':'sum',
      'Total Email': 'sum',
      'Total':'sum'
  }
  userapp = df.copy()

  userapp["Total Google"]    = userapp["Google DL (Bytes)"] + userapp["Google UL (Bytes)"]
  userapp["Total Youtube"]   = userapp["Youtube DL (Bytes)"] + userapp["Youtube UL (Bytes)"]
  userapp["Total Netflix"]   = userapp["Netflix DL (Bytes)"] + userapp["Netflix UL (Bytes)"]
  userapp["Total Email"]     = userapp["Email DL (Bytes)"] + userapp["Email UL (Bytes)"]
  userapp["Total Gaming"]    = userapp["Gaming DL (Bytes)"] + userapp["Gaming UL (Bytes)"]
  userapp["Total Social Media"] = userapp["Social Media DL (Bytes)"] + userapp["Social Media UL (Bytes)"]
  userapp["Total Other"]     = userapp["Other DL (Bytes)"] + userapp["Other UL (Bytes)"]
  userapp['Total']           = userapp['Total UL (Bytes)'] + userapp['Total DL (Bytes)']

  # Remove Outliers
  columns = ['Total Google', 'Total Youtube', 'Total Netflix', 'Total Email', 'Total Gaming', 'Total Social Media', 'Total Other', 'Total']
  
  
    
  user_behaviour = userapp.groupby('MSISDN/Number').agg(aggrigate)
  user_behaviour = utils.fix_outlier(user_behaviour, columns)
  return user_behaviour

def bivariant(user_behaviour):
  fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8)) = plt.subplots(2, 4,figsize=(15,8))
  # plot_scatter(user_behaviour.sample(1000), "Total", "Total Social Media", "Total Vs Social Media",ax1, "", "")

  def bivariant_sactter(df, x_col, y_col, ax):
    sns.scatterplot(data = df, x=x_col, y=y_col, ax=ax)

  sample_df = user_behaviour.sample(1000)
  # sns.scatterplot(data = sample_df)
  bivariant_sactter(sample_df, 'Total', 'Total Social Media', ax1)
  bivariant_sactter(sample_df, 'Total', 'Total Google', ax2)
  bivariant_sactter(sample_df, 'Total', 'Total Youtube', ax3)
  bivariant_sactter(sample_df, 'Total', 'Total Netflix', ax4)
  bivariant_sactter(sample_df, 'Total', 'Total Gaming', ax5)
  bivariant_sactter(sample_df, 'Total', 'Total Email', ax6)
  bivariant_sactter(sample_df, 'Total', 'Total Other', ax7)
  # bivariant_sactter(sample_df, 'Total', 'Total', ax8)
  st.pyplot()

def univriant(user_df):
  fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8)) = plt.subplots(2, 4,figsize=(15,8))

  user_df = user_df.sample(1000)
  sns.displot(data=user_df, x="Total Google", color="Green", ax=ax1)
  sns.displot(data=user_df, x="Total Youtube", color="Green", ax=ax2)

  ax1.hist(user_df['Total Google'])
  sns.displot(data=user_df, x='Total Google', color="red", kde=True, ax=ax1)
  ax1.set_title("Total Google")
  
  ax2.hist(user_df['Total Email'])
  ax2.set_title("Total Email")

  ax3.hist(user_df['Total Youtube'])
  ax3.set_title("Total Youtube")

  ax4.hist(user_df['Total Netflix'])
  ax4.set_title("Total Netflix")

  ax5.hist(user_df['Total Gaming'])
  ax5.set_title("Total Gaming")

  ax6.hist(user_df['Total Social Media'])
  ax6.set_title("Total Social Media")

  ax7.hist(user_df['Total Email'])
  sns.displot(data=user_df, x='Total Email', color="green", kde=True, ax=ax7)
  ax7.set_title("Total Netflix")

  ax8.hist(user_df['Total Other'])
  sns.displot(data=user_df, x='Total Other', color="green", kde=True, ax=ax8)
  ax8.set_title("Total Other")
  st.pyplot()
def app_engagement(user_df):
  fix, ax = plt.subplots(1, 1, figsize=(12,7))
  engagement = user_df.copy()
  data = []
  # Social Media engagement
  columns = engagement.columns.tolist()[:-1]

  for column in columns:
      data.append(engagement[column].sum())

  data_df = pd.DataFrame({"Application": columns, "counts":data})
  data_df.sort_values(by='counts', ascending=False)[:3]
  sns.barplot(data = data_df, x='Application', y='counts', ax=ax)
  plt.show()
def plot_heatmap(df:pd.DataFrame, title:str, cbar=False)->None:
  plt.figure(figsize=(12, 7))
  sns.heatmap(df, annot=True, cmap='viridis', vmin=0, vmax=1, fmt='.2f', linewidths=.7, cbar=cbar )
  plt.title(title, size=18, fontweight='bold')
  st.pyplot()
def engagement_analysis():
  file_name = 'data/clean_df_tel1.csv'
  df_clean = pd.read_csv(file_name)
  print(" I am at engahement")

  #st.write("### User Engagement Analysis")
  st.write("the following are results of the agrregation of each application based on the MSISDN/Number")
  user_df = get_user_related_columns(df_clean)
  st.write(user_df.head(7))
  # correlation among each application
  correlation = user_df.corr()
  st.write(" the correlation among each application in the given datasets")
  plot_heatmap(correlation, 'Correlation B/n  Applications')
  st.write("### The Univariant analysis of the applications")
  univriant(user_df)
  st.write("### The Bivariant plot which shows the relatioship between the total with each application")
  bivariant(user_df)

  app_engagement(user_df)

  st.write("### The Engagment Analysis of each application using plot")
  st.pyplot()

  st.write("The aggregation shows most of the customers of the telecommunications are engaged in game application.\
    Close to 1,314,797,820 bytes of data are used for the gamming application.\
    The correlation shows most of the applications are having small relationship which indicates the customers are most of the time focusing on specific application\
                  Here the amount of the bytes used in the Total game and the Total byte have almost close relationship which proves most of the people are investing their data on gaming application.")
