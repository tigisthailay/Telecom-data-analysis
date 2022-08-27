#System Modules
import os
import sys
sys.path.append(os.path.abspath(os.path.join('..')))

import warnings
warnings.filterwarnings('ignore')

# importing packages
import streamlit as st
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import script.ploting_fun as plot
#from scripts import file
import seaborn as sns
#Exprience Analysis
# def null_percentage(df):
#     number_of_rows, number_of_columns = df.shape
#     df_size = number_of_rows * number_of_columns
    
#     null_size = (df.isnull().sum()).sum()
#     percentage = round((null_size / df_size) * 100, 2)
#     st.write("Data Fraame contain null values of:",percentage)
def plot_bar(df:pd.DataFrame, x_col:str, y_col:str, title:str, xlabel:str, ylabel:str)->None:
  plt.figure(figsize=(12, 7))
  sns.barplot(data = df, x=x_col, y=y_col)
  plt.title(title, size=20)
  plt.xticks(rotation=75, fontsize=14)
  plt.yticks( fontsize=14)
  plt.xlabel(xlabel, fontsize=16)
  plt.ylabel(ylabel, fontsize=16)
  plt.show()
  st.pyplot()
def experiance_analysis():
  #Read the csv file
  st.write("The User Experience Analysis in the Telecom campany")
  file_name = 'data/tele-data.csv'
  df_expre = pd.read_csv(file_name)
  new_df = df_expre[['MSISDN/Number', 'Handset Type','TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)',\
                         'Avg RTT DL (ms)', 'Avg RTT UL (ms)',\
                         'Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)']]
  #null_percentage(new_netwok_df)
  # new_netwok_df.isnull().sum()
  # ## Fill Mising Values
  for col in new_df.columns:
    if(new_df[col].isnull().sum()):
      new_df[col] = new_df[col].fillna(new_df[col].mode()[0])
  # null_percentage(new_netwok_df)
  # new_netwok_df.isnull().sum()
  new_df['Total TCP Retrans'] = new_df['TCP DL Retrans. Vol (Bytes)'] +\
                                       new_df['TCP UL Retrans. Vol (Bytes)']
  new_df['Total Throughput'] = new_df['Avg Bearer TP DL (kbps)'] +\
                                      new_df['Avg Bearer TP DL (kbps)']
  new_df['Total RTT'] = new_df['Avg RTT DL (ms)'] + new_df['Avg RTT UL (ms)']
  st.write(new_df.head())
  aggregate = {'Handset Type':'first','Total TCP Retrans':'sum', 'Total Throughput':'sum', 'Total RTT':'sum'}
  columns = ['MSISDN/Number','Bearer Id','Handset Type', 'Total TCP Retrans', 'Total Throughput', 'Total RTT']
  data_per_user_df = new_df.groupby('MSISDN/Number').agg(aggregate).reset_index()
  st.write(data_per_user_df.head())
  # top 5
  result = data_per_user_df.sort_values(by='Total TCP Retrans', ascending=False)[:100]
  plot_bar(result, result['Handset Type'], result['Total TCP Retrans'], 'Highest Total TCP Retrans Handsets','','')
  # Bottom 5
  st.write(data_per_user_df.sort_values(by='Total TCP Retrans', ascending=True)[:5])
  handset_throughput = data_per_user_df.groupby('Handset Type').agg({'Total Throughput': 'sum'}).reset_index()
  st.write(handset_throughput.sort_values(by='Total Throughput', ascending=False).head(5))
  handset_rtt = data_per_user_df.groupby('Handset Type').agg({'Total RTT': 'sum'}).reset_index()
  st.write(handset_rtt.sort_values(by='Total RTT', ascending=False).head(5))
  handset= data_per_user_df['Handset Type'].unique()
  data_cluster_df = data_per_user_df.copy()
  data_cluster_df.drop('Handset Type', axis=1, inplace=True)
  data_cluster_df = data_cluster_df.set_index('MSISDN/Number')
  st.write(data_cluster_df.head())
  st.write("### The Experience Analysis of the telecom company ")
  st.write("In this task it has been tried to identify which company has high TCP Retrans and accordingly Huawei and Apple are the first and second one.\
While the total throughput of iApple handset is greater by 21kb when it is compared with Huawei.\ "
)
