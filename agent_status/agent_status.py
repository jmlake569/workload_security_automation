import requests
import json
import csv

REGION = "<YOUR-CLOUD-ONE-REGION-HERE>"
C1_API_KEY = "<YOUR-API-KEY-HERE>"

#API endpoint URL and headers
c1 = f"https://workload.{REGION}.cloudone.trendmicro.com/api/computers"
c1_headers = {"api-version": "v1", "Content-Type": "application/json", "Authorization": C1_API_KEY}

try:
    #make the API request
    response = requests.get(c1, headers=c1_headers)
    response.raise_for_status()  # Raise an exception if the response status code is not 2xx
    
    #parse the JSON response
    data = json.loads(response.content)
    
    if "computers" in data:
        computers = data["computers"]
    else:
        raise KeyError("The 'computers' key was not found in the response.")
    
    #define CSV file name
    csv_filename = "computer_data.csv"
    
    #write extracted data to CSV
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["HostName", "DisplayName", "Description", "LastIPUsed", "Platform", "AgentStatusMessages"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for computer in computers:
            host_name = computer.get("hostName", "")
            display_name = computer.get("displayName", "")
            description = computer.get("description", "")
            last_ip_used = computer.get("lastIPUsed", "")
            platform = computer.get("platform", "")
            
            agent_status_messages = computer["computerStatus"].get("agentStatusMessages", [])
            agent_status_messages = ", ".join(agent_status_messages)
            
            writer.writerow({
                "HostName": host_name,
                "DisplayName": display_name,
                "Description": description,
                "LastIPUsed": last_ip_used,
                "Platform": platform,
                "AgentStatusMessages": agent_status_messages
            })
    
    print("Data has been successfully written to the CSV file.")
    
except requests.exceptions.RequestException as e:
    print(f"Request to the API failed: {e}")
except json.JSONDecodeError as e:
    print(f"Failed to parse JSON response: {e}")
except KeyError as e:
    print(f"Key error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")