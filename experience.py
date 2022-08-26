import os
import sys
sys.path.append(os.path.abspath(os.path.join('..')))

import warnings
warnings.filterwarnings('ignore')
import streamlit as st
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import script.ploting as plot
#from script import file
import seaborn as sns
#Exprience Analysis
def null_percentage(df):
    number_of_rows, number_of_columns = df.shape
    df_size = number_of_rows * number_of_columns
    
    null_size = (df.isnull().sum()).sum()
    percentage = round((null_size / df_size) * 100, 2)
    st.write("Data Fraame contain null values of:",percentage)
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
def run_experiance():
  #Read the csv file
  st.write("## User Experience Analysis")
  file_name = 'C:/Users/user/Desktop/Telecommunication/data/Week1_challenge_data_source(CSV).csv'
  df_task_3 = pd.read_csv(file_name)
  new_netwok_df = df_task_3[['MSISDN/Number', 'Handset Type','TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)',\
                         'Avg RTT DL (ms)', 'Avg RTT UL (ms)',\
                         'Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)']]
  null_percentage(new_netwok_df)
  new_netwok_df.isnull().sum()
  ## Fill Mising Values
  for col in new_netwok_df.columns:
    if(new_netwok_df[col].isnull().sum()):
      new_netwok_df[col] = new_netwok_df[col].fillna(new_netwok_df[col].mode()[0])
  null_percentage(new_netwok_df)
  new_netwok_df.isnull().sum()
  new_netwok_df['Total TCP Retrans'] = new_netwok_df['TCP DL Retrans. Vol (Bytes)'] +\
                                       new_netwok_df['TCP UL Retrans. Vol (Bytes)']
  new_netwok_df['Total Throughput'] = new_netwok_df['Avg Bearer TP DL (kbps)'] +\
                                      new_netwok_df['Avg Bearer TP DL (kbps)']
  new_netwok_df['Total RTT'] = new_netwok_df['Avg RTT DL (ms)'] + new_netwok_df['Avg RTT UL (ms)']
  st.write(new_netwok_df.head())
  aggregate = {'Handset Type':'first','Total TCP Retrans':'sum', 'Total Throughput':'sum', 'Total RTT':'sum'}
  columns = ['MSISDN/Number','Bearer Id','Handset Type', 'Total TCP Retrans', 'Total Throughput', 'Total RTT']
  network_per_user_df = new_netwok_df.groupby('MSISDN/Number').agg(aggregate).reset_index()
  st.write(network_per_user_df.head())
  # top 5
  result = network_per_user_df.sort_values(by='Total TCP Retrans', ascending=False)[:100]
  plot_bar(result, result['Handset Type'], result['Total TCP Retrans'], 'Highest Total TCP Retrans Handsets','','')
  # Bottom 5
  st.write(network_per_user_df.sort_values(by='Total TCP Retrans', ascending=True)[:5])
  handset_throughput = network_per_user_df.groupby('Handset Type').agg({'Total Throughput': 'sum'}).reset_index()
  st.write(handset_throughput.sort_values(by='Total Throughput', ascending=False).head(5))
  handset_rtt = network_per_user_df.groupby('Handset Type').agg({'Total RTT': 'sum'}).reset_index()
  st.write(handset_rtt.sort_values(by='Total RTT', ascending=False).head(5))
  handset= network_per_user_df['Handset Type'].unique()
  net_cluster_df = network_per_user_df.copy()
  net_cluster_df.drop('Handset Type', axis=1, inplace=True)
  net_cluster_df = net_cluster_df.set_index('MSISDN/Number')
  st.write(net_cluster_df.head())
  st.write("## Experience Analytics Results")
  st.write("It is figured out on graph d) Huawei has high TCP Retrans and Apple is the second one.\
While the total throughput of iApple handset is greater by 21kb when it is compared with Huawei.\
In addition to this the average TCP trans of Apple is about 60,460 kbps and average TCP trans of Apple is about 16,996.00 kbps.\
Having this information, I recommend the investor to sell the Apple handset to increase the profit of the telecom. ")
