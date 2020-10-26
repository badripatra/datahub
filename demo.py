import os
import sys
import time


if sys.argv[1] == 'start':
    os.system("docker-compose up -d")
    time.sleep(30)
    os.system("nohup python consumer.py >> ./consumer_logs.log 2>&1 &")
    os.system("nohup python producer.py >> ./producer_logs.log 2>&1 &")

elif sys.argv[1] == 'stop':
    os.system("kill -9 `ps -ef|grep -v grep|grep 'python consumer'|awk '{print $2}'` > /dev/null 2>&1")
    os.system("kill -9 `ps -ef|grep -v grep|grep 'python producer'|awk '{print $2}'` > /dev/null 2>&1")
    os.system("docker-compose stop")
    os.system("docker-compose rm -f")
    #os.system("docker system prune -a -f --volumes")