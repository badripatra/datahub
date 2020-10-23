import os
from influxdb import InfluxDBClient
from time import time
import subprocess



client = InfluxDBClient(host='172.28.1.1', port=8086,username='datahub_influx',
                        password ='datahub_influx')

def ShellProcess(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.communicate()
    return output[0].strip()

def push_data_influx(asup_id, job_name,service_name, verification_point,expected,actual,status,env):

    client.switch_database('datahub')
    current_time = int(time()) * 1000

    if status == "Pass":
        json_body = [

                {
                  "measurement": "automation_results",
                  "time": current_time,
                  "fields": {"asup_id":asup_id,
                             "job_name":job_name,
                             "service_name":service_name,
                             "verification_point":verification_point,
                             "expected": expected,
                             "actual": actual,
                             "status": status,
                             "count": 1,
                             "env":env}
                }
              ]
    elif status == "Fail":
        json_body = [

            {
                "measurement": "automation_results",
                "time": current_time,
                "fields": {"asup_id": asup_id,
                           "job_name": job_name,
                           "service_name": service_name,
                           "verification_point": verification_point,
                           "expected": expected,
                           "actual": actual,
                           "status": status,
                           "countErr": 1,
                           "env": env}
            }
        ]

    client.write_points(json_body, time_precision='ms')


def get_folder_location_asup(asup_id):
    folder_location = "/"+asup_id[0:4]+"-"+asup_id[4:6]+"-"+asup_id[6:8]+"/"+asup_id[8:10]+"/"+asup_id[10:12]+\
                  "/"+asup_id[12:14]+"/"+asup_id[14:16]+"/"+asup_id
    return folder_location


def check_log_presence(job_name, service_name, asup_id):

    job_location = "/logs/"+job_name+".log"
    command = "grep "+asup_id+" "+job_location
    expected = "ASUP ID : "+asup_id+ " Processed Successfully"
    actual = ShellProcess(command)

    if actual == expected:
        result = "Pass"
    else:
        result = "Fail"


    push_data_influx(asup_id, job_name, service_name, "check_log_presence",expected,actual,result,"stg")

    return result

