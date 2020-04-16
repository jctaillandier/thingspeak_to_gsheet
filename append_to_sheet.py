import oauth2client
import json
import gspread
from  oauth2client.service_account import ServiceAccountCredentials
import wget
import argparse
import csv
import datetime
import os

pwd = os.getcwd()
print(pwd)
temp_file_name = f'{pwd}/tmp_file.csv'
temp_file_mateo = f'{pwd}/tmp_file_mateo.csv'

if os.path.isfile(temp_file_name):
    os.remove(temp_file_name)

if os.path.isfile(temp_file_mateo):
    os.remove(temp_file_mateo)

file = open(f'{pwd}/last_date', 'r') 
last_date =  file.read() 
file.close()

# Get current time to use as `end` value in thingspeak api
now = datetime.datetime.now()
date_time = str(now).split(' ')
now = f"{date_time[0]}%20{date_time[1].split('.')[0]}"

url= f'https://api.thingspeak.com/channels/562202/feeds.csv?api_key={os.environ["TS_READ_API"]}&start={last_date}&timezone=America%2FNew_York' 
url_mateo = f"https://api.thingspeak.com/channels/254746/feeds.csv?api_key=&start={last_date}&timezone=America%2FNew_York"

wget.download(url, out=f"{temp_file_name}")
wget.download(url_mateo, out=f"{temp_file_mateo}")

# json_key = json.load(open('wanet-api-sensors.json')) # json credentials you downloaded earlier
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(f'{pwd}/wanet-api-sensors.json',
                        scopes=scope) # get email and key from creds

file = gspread.authorize(credentials) # authenticate with Google

sheet = file.open("wanet_data_write").worksheet('jc_machine') # open sheet

data = []
with open(f'{temp_file_name}', newline='') as csvfile:
    # spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for i,row in enumerate(csv.reader(csvfile)):
        if i !=0:
            data.append(row[:6])

sheet.append_rows(data)

sheet_mateo = file.open("wanet_data_write").worksheet('cp_mr_machine') # open sheet

data_mateo = []
with open(f'{temp_file_mateo}', newline='') as csvfile_mateo:
    # spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for i,row in enumerate(csv.reader(csvfile_mateo)):
        if i !=0:
            data_mateo.append(row)
# import pdb; pdb.set_trace()
sheet_mateo.append_rows(data_mateo)

os.remove(f'{temp_file_name}')
os.remove(f'{temp_file_mateo}')

file = open(f'{pwd}/last_date', 'w') 
file.write(now) 

