from kafka import KafkaConsumer
from json import loads
from time import sleep
import requests
import json
import glob
import yaml


job_list = []
automation_jobs =glob.glob("./automation_jobs/*.yaml")
for each_file in automation_jobs:
    with open(each_file) as job_details:
        job_details = yaml.load(job_details.read())
        if job_details["execute"]:
            job_list.append(job_details)


consumer = KafkaConsumer(
    'topic_test',
    bootstrap_servers=['0.0.0.0:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

base_verification_url = "http://0.0.0.0:8083/api/verifiation/"
headers = {'content-type': 'application/json'}

for event in consumer:
    event_data = event.value
    asup_type = event_data["asup_type"]
    asup_id = event_data["asup_id"]

    for each_item in job_list:

        job_filter = each_item["asup_type"]

        if job_filter == asup_type:
            job_name = each_item["automation_jobname"]
            service_name = each_item["service_name"]
            method = each_item["verfication"]["method"]
            url = base_verification_url + method

            data = {'asup_id':asup_id, 'job_name':job_name, 'service_name': service_name}
            response = requests.post(url, data= json.dumps(data),headers=headers)
            print (url)
            print (data)
            print (response.text)
            sleep(1)

