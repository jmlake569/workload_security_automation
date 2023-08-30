import requests
import json
import csv

REGION = "<YOUR-CLOUD-ONE-REGION-HERE>"
C1_API_KEY = "<YOUR-API-KEY-HERE>"

c1 = f"https://workload.{REGION}.cloudone.trendmicro.com/api/computers"
c1_headers = {"api-version": "v1", "Content-Type": "application/json", "Authorization": C1_API_KEY}

response = requests.get(c1, headers=c1_headers)
data = json.loads(response.content)

#extracted data
computers = data["computers"]

#define CSV file name
csv_filename = "computer_data.csv"

#write extracted data to CSV
with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
    fieldnames = ["HostName", "DisplayName", "Description", "LastIPUsed", "Platform", "AgentStatusMessages"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for computer in computers:
        host_name = computer["hostName"]
        display_name = computer["displayName"]
        description = computer["description"]
        last_ip_used = computer["lastIPUsed"]
        platform = computer["platform"]
        agent_status_messages = ", ".join(computer["computerStatus"]["agentStatusMessages"])
        
        writer.writerow({
            "HostName": host_name,
            "DisplayName": display_name,
            "Description": description,
            "LastIPUsed": last_ip_used,
            "Platform": platform,
            "AgentStatusMessages": agent_status_messages
        })

print(f"Data has been written to '{csv_filename}'")