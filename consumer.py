from kafka import KafkaConsumer
from json import loads
from time import sleep
import requests
import json

consumer = KafkaConsumer(
    'topic_test',
    bootstrap_servers=['0.0.0.0:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)
for event in consumer:
    event_data = event.value
    # Do whatever you want
    asup_id = event_data["asup_id"]
    job_name = event_data["job_name"]

    url = "http://0.0.0.0:8083/api/verifiation/check_nfs_presence"
    data = {'asup_id':asup_id, 'job_name':job_name}
    headers = {'content-type': 'application/json'}

    response = requests.post(url, data= json.dumps(data),headers=headers)
    print (url)
    print (data)
    print (response.text)

    sleep(1)
