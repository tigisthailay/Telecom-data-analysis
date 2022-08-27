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



page = option_menu('Menu', ['Main', 'User_Overview','User_Engagement', 'User_Experience', 'User_Satisfaction'],
                              icons=['house', 'bi-currency-exchange','bi-cloud-check-fill', 'bi-briefcase-fill',
                              'bi-check-square-fill'], menu_icon="cast", default_index=1)
page
    
    
df = pd.read_csv('C:/Users/user/Downloads/Telecom-data-analysis/data/cleaned_data.csv')
    
overview = OverviewAnalysis(df)
    
satisfy = SatisfuctionAnalysis(df)
  
if(page == 'main'):
  main1.run()
elif(page == 'User_Overview'):
  overview.overview_analysis()
elif(page == 'User_Engagement'):
  engage.engagement_analysis()
elif(page == 'User_Experience'):
  expriance.experiance_analysis()
elif(page == 'User_Satisfaction'):
  satisfy.satisfaction_analysis()
else:
 main1.run()
