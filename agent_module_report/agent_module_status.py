import requests
import json
import pandas as pd

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
    #get the hostnames
    hostname = computer.get('hostName', 'Not available')

    #initialize default values
    integrity_monitoring_info = 'Not available'
    intrusion_prevention_info = 'Not available'
    anti_malware_info = 'Not available'
    agent_status = 'Not available'
    web_reputation_info = 'Not available'
    device_control_info = 'Not available'
    activity_monitoring_info = 'Not available'
    application_control_info = 'Not available'
    firewall_info = 'Not available'
    log_inspection_info = 'Not available'


    #get the integrity_monitoring data
    integrity_monitoring = computer.get('integrityMonitoring')
    if integrity_monitoring:
        module_status = integrity_monitoring.get('moduleStatus')
        if module_status:
            agent_status = module_status.get('agentStatus', 'Not available')
            integrity_monitoring_info = module_status.get('agentStatusMessage', 'Not available')

    #get the intrusion_prevention data
    intrusion_prevention = computer.get('intrusionPrevention')
    if intrusion_prevention:
        intrusion_module_status = intrusion_prevention.get('moduleStatus')
        if intrusion_module_status:
            intrusion_prevention_info = intrusion_module_status.get('agentStatusMessage', 'Not available')

    #get the anti_malware data
    anti_malware = computer.get('antiMalware')
    if anti_malware:
        anti_malware_module_status = anti_malware.get('moduleStatus')
        if anti_malware_module_status:
            anti_malware_info = anti_malware_module_status.get('agentStatusMessage', 'Not available')

    #get the web_reputation data
    web_reputation = computer.get('webReputation')
    if web_reputation:
        web_reputation_module_status = web_reputation.get('moduleStatus')
        if web_reputation_module_status:
            web_reputation_info = web_reputation_module_status.get('agentStatusMessage', 'Not available')

    #get the device_control data
    device_control = computer.get('deviceControl')
    if device_control:
        device_control_module_status = device_control.get('moduleStatus')
        if device_control_module_status:
            device_control_info = device_control_module_status.get('agentStatusMessage', 'Not available')

    #get the activity_monitoring data
    activity_monitoring = computer.get('activityMonitoring')
    if activity_monitoring:
        activity_monitoring_module_status = activity_monitoring.get('moduleStatus')
        if activity_monitoring_module_status:
            activity_monitoring_info = activity_monitoring_module_status.get('agentStatusMessage', 'Not available')
    
    #get the application_control data
    application_control = computer.get('applicationControl')
    if application_control:
        application_control_module_status = activity_monitoring.get('moduleStatus')
        if application_control_module_status:
            application_control_info = application_control_module_status.get('agentStatusMessage', 'Not available')

    #get the firewall data
    firewall = computer.get('firewall')
    if firewall:
        firewall_module_status = firewall.get('moduleStatus')
        if firewall_module_status:
            firewall_info = firewall_module_status.get('agentStatusMessage', 'Not available')
    
    #get the log_inspection data
    log_inspection = computer.get('logInspection')
    if log_inspection:
        log_inspection_module_status = log_inspection.get('moduleStatus')
        if log_inspection_module_status:
            log_inspection_info = log_inspection_module_status.get('agentStatusMessage', 'Not available')

    #add this data to a dictionary and append it to computers_data
    computer_data = {
        'hostName': hostname,
        'agentStatus': agent_status,
        'antiMalware': anti_malware_info,
        'webReputation': web_reputation_info,
        'deviceControl': device_control_info,
        'activityMonitoring': activity_monitoring_info,
        'applicationControl': application_control_info,
        'firewall': firewall_info,
        'integrityMonitoring': integrity_monitoring_info,
        'intrusionPrevention': intrusion_prevention_info,
        'applicationControl': application_control_info,
        'logInspection': log_inspection_info,
    }
    computers_data.append(computer_data)

#convert the list of computer data to DataFrame
df_computers = pd.DataFrame(computers_data)

#reorder columns in DataFrame
df_computers = df_computers[['hostName', 'agentStatus', 'antiMalware', 'webReputation', 'deviceControl', 'activityMonitoring', 'applicationControl', 'firewall', 'integrityMonitoring', 'intrusionPrevention', 'logInspection']]

#save as CSV
df_computers.to_csv('agent_module_status.csv', index=False)