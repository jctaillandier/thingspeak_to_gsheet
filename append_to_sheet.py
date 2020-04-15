import oauth2client
import json
import gspread
from  oauth2client.service_account import ServiceAccountCredentials
import wget
import argparse
import csv
import datetime
import os

def main():
    temp_file_name = './tmp_file.csv'
    if os.path.isfile(temp_file_name):
        os.remove(temp_file_name)

    file = open('last_date', 'r') 
    last_date =  file.read() 
    file.close()
    
    # Get current time to use as `end` value in thingspeak api
    now = datetime.datetime.now()
    date_time = str(now).split(' ')
    now = f"{date_time[0]}%20{date_time[1].split('.')[0]}"

    url= f'https://api.thingspeak.com/channels/562202/feeds.csv?api_key={os.environ["TS_READ_API"]}&start={last_date}&timezone=America%2FNew_York' 

    wget.download(url, out=f"{temp_file_name}")

    # json_key = json.load(open('wanet-api-sensors.json')) # json credentials you downloaded earlier
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('./wanet-api-sensors.json',
                            scopes=scope) # get email and key from creds

    file = gspread.authorize(credentials) # authenticate with Google
    sheet = file.open("wanet_data_write").worksheet('jc_machine') # open sheet

    data = []
    with open(f'tmp_file.csv', newline='') as csvfile:
        # spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for i,row in enumerate(csv.reader(csvfile)):
            if i !=0:
                data.append(row[:6])

    sheet.append_rows(data)

    file = open('last_date', 'w') 
    file.write(now) 

    return 

if __name__ == "__main__":
    main()