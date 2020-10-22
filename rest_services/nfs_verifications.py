import os
from influxdb import InfluxDBClient
from time import time

client = InfluxDBClient(host='172.28.1.1', port=8086,username='datahub_influx',
                        password ='datahub_influx')


def push_data_influx(job_name,service_name, verification_point,expected,actual,status,env):

    client.switch_database('datahub')
    current_time = int(time()) * 1000

    json_body = [

            {
              "measurement": "automation_results",
              "time": current_time,
              "fields": {"job_name":job_name,
                         "service_name":service_name,
                         "verification_point":verification_point,
                         "expected": expected,
                         "actual": actual,
                         "status": status,
                         "env":env}
            }
          ]

    client.write_points(json_body, time_precision='ms')


def get_folder_location_asup(asup_id):
    folder_location = "/"+asup_id[0:4]+"-"+asup_id[4:6]+"-"+asup_id[6:8]+"/"+asup_id[8:10]+"/"+asup_id[10:12]+\
                  "/"+asup_id[12:14]+"/"+asup_id[14:16]+"/"+asup_id
    return folder_location


def check_nfs_presence(job_name, service_name, asup_id):

    job_location = "/nfsvolume/"+job_name
    asup_derived_path = get_folder_location_asup(asup_id)
    expected = job_location + asup_derived_path
    isFile = os.path.isfile(job_location + asup_derived_path)
    if isFile:
        result = "Pass"
        actual = expected
    else:
        result = "Fail"
        actual = ""

    push_data_influx(job_name, service_name, "check_nfs_presence",expected,actual,result,"stg")

    return result

