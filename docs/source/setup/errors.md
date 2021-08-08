# Frequent Errors and Solutions

- In case if Postresql port is already in use: `systemctl stop postgresql`
- Port errors
```bash
# command to check port usage
export PORTNO=8088
sudo lsof -i -P -n | grep LISTEN | grep $PORTNO

#command to kill all running docker instances
docker kill $(docker ps -q) 
```