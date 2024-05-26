# FusionSolar_Export_Script
Python Script used to download pv plant data from Huawei FusionSolar API (with personal username &amp; password)

Acquires data from the API in the form of a json file and export a csv file, where each line corresponds
to a specific timestamp and provides energy data from the PV plant inverters for said timestamp.

In order for the script to export data, there must be an input of:
username, password, PV plant station(name & code), 
starting date, days interval and total amount of days for acquiring data.
