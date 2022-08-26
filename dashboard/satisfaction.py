import os
import sys
sys.path.append(os.path.abspath(os.path.join('..')))

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import script.ploting as plot
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
#User Statisfaction Analysis
def run_satisfaction():
  st.write("## Satisfaction Analysis")
  file_name = 'C:/Users/user/Desktop/Telecommunication/data/cleaned_data.csv'
  data = pd.read_csv(file_name)
  #Aggregate per user the following information in the column
  df_clean = data.copy()
  aggregate = {"Bearer Id": 'count', 'Dur. (ms).1':'sum', 'Total UL (Bytes)': 'sum', 'Total DL (Bytes)': 'sum'}
  aggregation_result = df_clean.groupby('MSISDN/Number').agg(aggregate)
  aggregation_result.head()
  #Aggregate the above metrics per customer id (MSISDN) and report the top 10 customers per engagement metric
  df_task2 = df_clean.copy()
  df_task2['Total'] = df_task2['Total UL (Bytes)'] + df_task2['Total DL (Bytes)']
  df_task2 = df_task2.groupby('MSISDN/Number')\
    .agg({"Bearer Id": "count", 'Dur. (ms).1':'sum', 'Total':'sum'})
  #Normalize each engagement metric and run a k-means (k=3) to classify customers in three groups of engagement.
  min_max_scaler = preprocessing.MinMaxScaler()
  df_values = df_task2.values
  scalled_values = min_max_scaler.fit_transform(df_values)
  df_normalized = pd.DataFrame(data=scalled_values, columns=df_task2.columns)
  kmeans = KMeans(n_clusters=3).fit(df_normalized)
  def null_percentage(df):
    number_of_rows, number_of_columns = df.shape
    df_size = number_of_rows * number_of_columns
    
    null_size = (df.isnull().sum()).sum()
    percentage = round((null_size / df_size) * 100, 2)
    return percentage
  #Read the cleaned csv file and store it on data
  file_name = 'data/Week1_challenge_data_source.csv'
  data = pd.read_csv(file_name)
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
  #---------
  new_netwok_df['Total TCP Retrans'] = new_netwok_df['TCP DL Retrans. Vol (Bytes)'] +\
                                       new_netwok_df['TCP UL Retrans. Vol (Bytes)']
  new_netwok_df['Total Throughput'] = new_netwok_df['Avg Bearer TP DL (kbps)'] +\
                                      new_netwok_df['Avg Bearer TP DL (kbps)']
  new_netwok_df['Total RTT'] = new_netwok_df['Avg RTT DL (ms)'] + new_netwok_df['Avg RTT UL (ms)']
  new_netwok_df.head()
  #---------
  aggregate = {'Handset Type':'first','Total TCP Retrans':'sum', 'Total Throughput':'sum', 'Total RTT':'sum'}
  columns = ['MSISDN/Number','Bearer Id','Handset Type', 'Total TCP Retrans', 'Total Throughput', 'Total RTT']
  network_per_user_df = new_netwok_df.groupby('MSISDN/Number').agg(aggregate).reset_index()
  network_per_user_df.head()
  handset= network_per_user_df['Handset Type'].unique()
  # catagory = {}
  # for index, each in enumerate(handset.tolist()):
  #     catagory[each] = index
  net_cluster_df = network_per_user_df.copy()
  net_cluster_df.drop('Handset Type', axis=1, inplace=True)
  net_cluster_df = net_cluster_df.set_index('MSISDN/Number')
   ## First normalize the Data, Then Cluster
  min_max_scaler = preprocessing.MinMaxScaler()
  network_values = net_cluster_df.values
  scalled_values = min_max_scaler.fit_transform(network_values)
  df_network_normalized = pd.DataFrame(data=scalled_values, columns=df_task2.columns)
  kmeans = KMeans(n_clusters=3).fit(df_normalized)
  cluster = kmeans.predict(df_network_normalized)
  experiance_df = network_per_user_df.copy()
  experiance_df['cluster-experiance']  = cluster
  experiance_df = experiance_df.set_index('MSISDN/Number')
  experiance_df.head()
  #Compute the minimum, maximum, average & total non- normalized metrics for each cluster.
  cluster = kmeans.predict(df_normalized)
  engagement_df = df_task2.copy()
  engagement_df['cluster-engagement']  = cluster
  cluster_group_df = engagement_df.groupby('cluster-engagement')
  cluster_0 = cluster_group_df.get_group(0)
  cluster_1 = cluster_group_df.get_group(1)
  cluster_2 = cluster_group_df.get_group(2)
  ## Engagement Score
  lowest_engagement = engagement_df.groupby('cluster-engagement').get_group(0).mean()
  st.write(lowest_engagement)
  def get_engagement_score(df, lowest):
    x = float(lowest['Bearer Id'])
    y = float(lowest['Dur. (ms).1'])
    z = float(lowest['Total'])
    new_df = df.copy()
    new_df['engagement score'] = ((df['Bearer Id'] - x)**2 + (df['Dur. (ms).1'] - y)**2 + (df['Total'] - z)**2)**0.5
    return new_df
  engagement_scored_df = get_engagement_score(engagement_df, lowest_engagement)
  st.write(engagement_scored_df.head())
  lowest_experiance = experiance_df.groupby('cluster-experiance').get_group(0).mean()
  st.write(lowest_experiance)
  def get_experiance_score(df, low):
    x = float(low['Total RTT'])
    y = float(low['Total TCP Retrans'])
    z = float(low['Total Throughput'])
    new_df = df.copy()
    new_df['experience score'] = ((df['Total RTT'] - x)**2 + (df['Total TCP Retrans'] - y)**2 \
                              + (df['Total Throughput'] - z)**2 )**0.5
    return new_df
  experiance_scored_df = get_experiance_score(experiance_df, lowest_experiance)
  st.write(experiance_scored_df.head())
  ##Task 4.2 - Consider the average of both engagement & experience scores as the satisfaction score & report the top 10 satisfied customer
  satisfaction_df = pd.merge(engagement_scored_df["engagement score"], experiance_scored_df['experience score'], on='MSISDN/Number')
  satisfaction_df['satisfaction score'] = (satisfaction_df['engagement score'] + satisfaction_df['experience score']) / 2
  st.write(satisfaction_df.sort_values(by='satisfaction score', ascending=False).head(5))
  #Task 4.3 - Build a regression model of your choice to predict the satisfaction score of a customer.
  regretion_df = pd.merge(engagement_df[['Bearer Id', 'Dur. (ms).1', 'Total']],\
                        experiance_df[['Total RTT','Total TCP Retrans', 'Total Throughput']],\
                       on='MSISDN/Number')
  regretion_df = pd.merge(regretion_df,satisfaction_df['satisfaction score'], on='MSISDN/Number' )
  st.write(regretion_df.head())
  X = regretion_df[['Bearer Id', 'Dur. (ms).1', 'Total','Total RTT','Total TCP Retrans', 'Total Throughput']].values
  X = StandardScaler().fit_transform(X)
  X.shape
  y = regretion_df[['satisfaction score']].values
  y = StandardScaler().fit_transform(y)
  y.shape
  model = LinearRegression().fit(X, y)
  st.write(model.score(X, y))
  st.write("## Satisfaction Analysis")
  st.write("Most of the user Telcco is more engaged and experienced on using the services.\
Thus, this shows that the user is satisfied by the Telcco service. \
The prediction of the developed model on the user satisfaction\
shows about 83.2% of the user is satisfied")
  

