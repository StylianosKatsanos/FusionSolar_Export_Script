# -*- coding: utf-8 -*-
"""
Last modified on Tue May 25 18:37:00 2024

@author: Stelios Katsanos  (katsanoss@outlook.com)

This file contains functions used in structuring the data acquired from the FusionSolar API
"""

import datetime

# Create dictionary that structures the data acquired from the API in json form
# It orders in based on Timestamp and inverter serial number

def create_daily_yield(data, timestamps, sn_list):
        
        daily_yield = {}
        
        for i in timestamps:
            
            daily_yield[i] = {}
            
            
            for j in sn_list:
                
                daily_yield[i][j] = None  #None is used for the cases that FusionSolar does not offer a specific timestamp
                
                
        # Each new day starts at 00:00 with 0 values for any inverter
        
        for l in sn_list:
            
            daily_yield[timestamps[0]][l] = 0
            
            
        # First input of data from day_cap parameter
          
        for i in data['data']:  
                
           daily_yield[i['collectTime']][i['sn']] =  i['dataItemMap']['day_cap']
           
        
        # Second input for data correction        
        
        for k in range(1, len(timestamps)):  
             
             for l in sn_list:
                 
                 if daily_yield[timestamps[k]][l] == None: #In case there no data use the previous to fill in
                     
                     daily_yield[timestamps[k]][l] = daily_yield[timestamps[k-1]][l]

            
        return daily_yield



# Main uses this function to add in case of pv plant with more than 10 inverters

def add_to_daily_yield(daily_yield, yield_data, sn_list, timestamps):
        
    for i in timestamps:
        
        for j in sn_list:
            
            daily_yield[i][j] = None
            
    for l in sn_list:
        
        daily_yield[timestamps[0]][l] = 0
        
   
    for i in yield_data['data']:
                
           daily_yield[i['collectTime']][i['sn']] =  i['dataItemMap']['day_cap']
           
    for k in range(1, len(timestamps)):  
         
         for l in sn_list:
             
             if daily_yield[timestamps[k]][l] == None:
                 
                 daily_yield[timestamps[k]][l] = daily_yield[timestamps[k-1]][l] 
                 
    return daily_yield


# Functions that add data for the first, last and inbetween days
    
def first_daily_yield(yield_data, sn_list, timestamps):
    
    first_entry = []
    first_entry.append(datetime.datetime.fromtimestamp(timestamps[0]/1000))
    for i in sn_list:
        first_entry.append(yield_data[timestamps[0]][i])
    first_entry.append(sum(first_entry[1:]))
    return(first_entry)
    

def last_daily_yield(yield_data, sn_list, timestamps):
    
    last_entry = []
    last_entry.append(datetime.datetime.fromtimestamp((timestamps[-1]+ 300000)/1000))
    for i in sn_list:
        last_entry.append(0)
    last_entry.append(sum(last_entry[1:]))
    return(last_entry)


def loop_daily_yield(yield_data, sn_list, timestamps, s_i, s_e):
    
    while s_e < len(timestamps)-1:
        entry = []
        entry.append(datetime.datetime.fromtimestamp(timestamps[s_e]/1000))
        for j in sn_list:
            ent = yield_data[timestamps[s_e]][j] - yield_data[timestamps[s_i]][j]
            if ent > 0:
                entry.append(ent)
            else:
                entry.append(0)
        entry.append(sum(entry[1:]))
        return entry
  
    
# Function that adds data without calculating any difference

def loop_daily_yield_cummulative(yield_data, sn_list, timestamps, s_e):
    
    while s_e < len(timestamps)-1:
        entry = []
        entry.append(datetime.datetime.fromtimestamp(timestamps[s_e]/1000))
        for j in sn_list:
            ent = yield_data[timestamps[s_e]][j]
            if ent > 0:
                entry.append(ent)
            else:
                entry.append(0)
        entry.append(sum(entry[1:]))
        return entry 