import os
import sys
sys.path.append(os.path.abspath(os.path.join('..')))
#import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu 
st.set_page_config(page_title='Telecom Data Analysis', page_icon=None, layout="centered", 
initial_sidebar_state="auto", menu_items=None)
# the pages
import dashboard.home as main1
from dashboard.user_analysis import OverviewAnalysis
import dashboard.engagement as engage
import dashboard.experience as expriance
from dashboard.satisfuction import SatisfuctionAnalysis


#with st.sidebar:
  #'Engagement', 'Experience', 'Satisfaction'
    #'bi-cloud-check-fill', 'bi-briefcase-fill','bi-check-square-fill'], menu_icon="cast", 
page = option_menu('Menu', ['Main', 'User_Overview','User_Engagement', 'User_Experience', 'User_Satisfaction'],
                              icons=['house', 'bi-currency-exchange','bi-cloud-check-fill', 'bi-briefcase-fill',
                              'bi-check-square-fill'], menu_icon="cast", default_index=1)
page
    
    
df = pd.read_csv('cleaned_data.csv')
    #file_name = 'data/telecom.csv'

    #df1 = pd.read_csv(file_name)

overview = OverviewAnalysis(df)
    #engagement = engagementAnalysis(df)
    #expriance = exprianceAnalysis(df1)
satisfy = SatisfuctionAnalysis(df)
    #df = pd.read_csv('data/clean_df_tel1.csv')
if(page == 'home'):
  main1.run()
elif(page == 'user_analysis'):
  overview.overview_analysis()
elif(page == 'engagement'):
  engage.engagement_analysis()
elif(page == 'experience'):
  expriance.experiance_analysis()
elif(page == 'satisfaction'):
  satisfy.satisfaction_analysis()
else:
 main1.run()
