#!/bin/bash
# ApplicationStart: Start Spring Boot application
set -e
nohup java -jar /home/ec2-user/app/demo-0.0.1-SNAPSHOT.jar > /home/ec2-user/app/app.log 2>&1 &
