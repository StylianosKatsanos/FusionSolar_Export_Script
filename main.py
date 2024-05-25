# -*- coding: utf-8 -*-
"""
Last modified on Tue May 25 18:37:00 2024

@author: Stelios Katsanos (katsanoss@outlook.com)

Python script that exports csv data from the FusionSolar API that contains inverter total produced energy
based on parameter for the plant, the inverter and the specific timestamp of the data  
"""

import csv
from datetime import timedelta
import datetime
import urllib3
import os
import requests
from api_access import login, get_data, get_sn_list
from json_create import  create_daily_yield, first_daily_yield, last_daily_yield, loop_daily_yield, add_to_daily_yield


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main(Station_name, Station_code, start_date, days_step, days_limit):
    
    base_dir = os.getcwd()
    folder_name = '\\' + Station_name  
    folder_path = os.path.join(base_dir + folder_name)
    if os.path.exists(folder_path):
        print('station folder already exists')
    else:
        os.mkdir(folder_path)
    

    file_name = Station_name + '_'  + str(start_date.year) + "_" + str(start_date.month) + '.csv'

    file_path = os.path.join(folder_path, file_name)


    #===================== Serial Numbers =======================================================#

    # Get sn list from API 

    sn_list = get_sn_list(Station_code)

    #===================== Create Data file =============================================#
    
    with open(file_path, 'w', newline = '') as outfile:
        
        names = ['Timestamp'] + sn_list + ['Sum']
        
        writer = csv.writer(outfile, delimiter=',') 
        
        writer.writerow(names)
        
        day_timer = 0
        
        # Inputing processed data -- Case where sn_list is more than 10 inverters
        
        while day_timer < days_limit:  
            
            if len(sn_list) > 10:
                
                loop_data, loop_timestamps  = get_data(start_date, days_step, sn_list[:10])
                
                loop_yield = create_daily_yield(loop_data, loop_timestamps, sn_list[:10])
                
                check = 10
                
                while check < len(sn_list):
                    
                    loop_data, loop_timestamps  = get_data(start_date, days_step, sn_list[check:check+10])
                    
                    loop_yield = add_to_daily_yield(loop_yield, loop_data, sn_list[check:check+10], loop_timestamps)
                    
                    check += 10
            
            else:
                
                loop_data, loop_timestamps  = get_data(start_date, days_step, sn_list)

                loop_yield = create_daily_yield(loop_data, loop_timestamps, sn_list)
            
            
            s_i = 0
            s_e = 3
            
            
            writer.writerow(first_daily_yield(loop_yield,sn_list,loop_timestamps))
            
            
            while s_e < len(loop_timestamps)-1:
                
                writer.writerow(loop_daily_yield(loop_yield,sn_list,loop_timestamps, s_i, s_e))
                
                s_i, s_e = s_i+3, s_e+3

                    
            day_timer += days_step
            start_date = start_date + timedelta(days=days_step)

        writer.writerow(last_daily_yield(loop_yield,sn_list,loop_timestamps))
        
    outfile.close()


if __name__ == "__main__":
    
    #====================== Credentials ====================================#
    
    user =  #Your Username
    
    password =  #Your Password
    
    #================================== Input ===========================================#

    # Date format:  (Year, Month, Day)
    start_date = datetime.datetime(2024,3,1)
    days_step = 1 # up to 3 days consequently
    days_limit = 10  # n - 1 of the days you want to calculate depending on the days step variable


    # Station Details
    
    Station_code =  #"The code of your Station"
    Station_name =  #"The name of your Station"

    #===================== Creating Session =================================================#

    session = requests.session()
    session.headers.update({'Connection': 'keep-alive', 'Content-Type': 'application/json'})

    #===================== Log In ========================================================#

    login(user, password)
    print("Access in plant", Station_name)
    
    #===================== Main Function ========================================================#

    main(Station_name,Station_code,start_date, days_step, days_limit)
        