from json import dumps
from kafka import KafkaProducer
import sched, time
import datetime
import os
import random

asup_type_list = ["dot-regular","dot-perf"]
base_volume = './nfsvolume/'

def create_folder(time_now):
    date_val = time_now.strftime("%Y-%m-%d")
    hour_val = time_now.strftime("%H")
    min_val = time_now.strftime("%M")
    second_val = time_now.strftime("%S")
    asup_id = str(date_val).replace("-","") + hour_val + min_val + second_val
    data = {"asup_id":asup_id}
    asup_type= random.choice(asup_type_list)

    if asup_type== "dot-regular":
        job_name = "testjob2"
    elif asup_type == "dot-perf":
        job_name = "testjob1"

    data["job_name"] = job_name
    source = base_volume +job_name
    dest = os.path.join(source, date_val, hour_val, min_val, second_val)
    if not os.path.exists(dest):
        os.makedirs(dest)  # creat dest dir
        with open(os.path.join(dest,asup_id),"w") as asup_file:
            asup_file.write("ASUP ID Processed")
    return data

def push_messages(sc):
    now = datetime.datetime.today()
    asip_id_generated = create_folder(now)
    print ("Mesage Publish : "+ str (asip_id_generated))
    producer.send('topic_test', value=asip_id_generated)
    s.enter(1, 1, push_messages, (sc,))

producer = KafkaProducer(
    bootstrap_servers=['0.0.0.0:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

s = sched.scheduler(time.time, time.sleep)
s.enter(1, 1, push_messages, (s,))
s.run()
