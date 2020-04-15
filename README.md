## ThingSpeak to Google Sheets

### 1. Much setup on Google API
    This is a struggle as multiple posts give various info, seems like it changes often

            - Go on google developer Console and enable GDrive AND GSheet API 
            - Create credentials and service accounts with read/write rights
            - Add the service account email to Google Sheet shared with email
            - This should help for the API calls: https://gspread.readthedocs.io/en/latest/user-guide.html#getting-all-values-from-a-worksheet-as-a-list-of-lists


### 2. Thingspeak has much docs for their API
            - Don't forget to add your api key to the call (got mine in environment vars on my machine)
            - Set timezone! That messed me up, still not sure what default is but definitely not EST