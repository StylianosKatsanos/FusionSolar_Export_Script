# -*- coding: utf-8 -*-
"""
Last modified on Tue May 25 18:37:00 2024

@author: Stelios Katsanos  (katsanoss@outlook.com)

This File contains functions used to access the FusionSolar API
and to request pv plant data
"""

import requests
from datetime import timedelta

#===================== Creating Session =================================================#

session = requests.session()
session.headers.update({'Connection': 'keep-alive', 'Content-Type': 'application/json'})

#===================== Login ===================================================#

# The login function is based on the code found in the Fusion_Solar_py package
# https://github.com/EnergieID/FusionSolar/blob/master/_login.py

def login(user, password):
    
    url_login = f'https://eu5.fusionsolar.huawei.com/thirdData/login'
    
    body_login = {
    'userName': user,
    'systemCode': password
    
    }
    
    session.cookies.clear()
    r = session.post(url=url_login, json=body_login, verify=False)
    r.raise_for_status()

    session.headers.update({'XSRF-TOKEN': r.cookies.get(name='XSRF-TOKEN')})
    
    print('Successfull login')


#===================== Get Data ===================================================#

# This function uses a start and timestamp in datetime form, a day step and a list of serial numbers of inverters
# and gets all data from specified inverters during a specific tme period


def get_data(start, step, sn_list):
    
    sns_keyword = ','.join(sn_list)   #serial number list into a string
    
    timestamps = [] 
    
    step_days = step
    
    #Start and end date use millisecond form
    
    end = int(start.timestamp()*1000) + (step_days * 86400000) - 300000  
    
    start_mil = int(start.timestamp()*1000) 
    
    while start_mil <= end:
        
        #Fill timestamps with 5 minute intervals before requesting the correspondiing data
        
        timestamps.append(start_mil) 
        
        start_mil += 300000  # = 5 minutes
    
    print('Getting data from ' + str(start) + ' to ' + str(start + timedelta(days=step)))
    
    url_data = f'https://eu5.fusionsolar.huawei.com/thirdData/getDevHistoryKpi'
    
    body_data = {
        'sns': sns_keyword, 
        'devTypeId': 1,
        'startTime':  int(start.timestamp()*1000),  # CANNOT us start_mil parameter,even though they are the same
        'endTime': end

    }
    
    data = session.post(url=url_data, json=body_data, verify=False)
    data.raise_for_status()
        
    return data.json(), timestamps


#Function Used for obtaining the serial numbers of the inverters in a pv plant

def get_sn_list(St_Code):
    
    #-----------------  Requesting Date --------------------------------------#
    
    url_dev_list = f'https://eu5.fusionsolar.huawei.com/thirdData/getDevList'
    
    body_dev_list = {
    "stationCodes": St_Code
    }
    
    data = session.post(url=url_dev_list, json=body_dev_list, verify=False)
    data.raise_for_status()
    
    #------------------  Obtaining Data --------------------------------------#
    
    data = data.json()
    
    sns = []
    
    for i in data['data']:
            
        if i["devTypeId"] == 1: # devTypeId is equal to 1 in case we are searching for the serial number of an inverter
           sns.append(i["esnCode"])
    
    return sns







