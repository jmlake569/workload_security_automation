import requests
import pandas as pd
import json
import datetime
from pprint import pprint

#this "DROP_LATEST" variable is used to drop the "latest" column from the CSV file which gives a "True" or "False" value if the agent is running latest updates or not.
DROP_LATEST = True

#cloud One workload security region and API Key
C1_REGION = '<YOUR_C1_REGION_HERE>'
C1_APIKEY = '<YOUR_API_KEY_HERE>'

#set the request parameters
c1 = f"https://workload.{C1_REGION}.cloudone.trendmicro.com/api/computers"
c1_headers = {"api-version": "v1", "Content-Type": "application/json", "Authorization": 'ApiKey ' + C1_APIKEY}

#send request and retreive data
response = requests.get(c1, headers=c1_headers)
data = json.loads(response.content)


computers_data = []

for computer in data.get('computers', []):
    #try to get the securityUpdates and antiMalware keys. If they don't exist, skip this computer.
    securityUpdates = computer.get('securityUpdates')
    if not securityUpdates:
        continue

    antiMalware = securityUpdates.get('antiMalware')
    if not antiMalware:
        continue

    #transform antiMalware into a list if it's a dictionary
    if isinstance(antiMalware, dict):
        securityUpdates['antiMalware'] = [antiMalware]
        
    #get the lastChanged timestamp and convert it from milliseconds to datetime
    lastChanged = securityUpdates.get('lastChanged')
    if lastChanged:
        #convert from milliseconds to seconds and then to datetime
        date = datetime.datetime.fromtimestamp(lastChanged / 1000)
        computer['lastChanged'] = date.isoformat()

    #add the modified computer data back to the list
    computers_data.append(computer)

#normalize JSON data for computers and securityUpdates -> antiMalware
df_computers = pd.json_normalize(data=computers_data, record_path=['securityUpdates', 'antiMalware'], meta=['hostName', 'lastChanged'], errors='ignore')

#drop the latest column
if DROP_LATEST and 'latest' in df_computers.columns:
    df_computers.drop('latest', axis=1, inplace=True)

#save as CSV
df_computers.to_csv('agent_pattern_status.csv', index=False)