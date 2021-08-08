# Databases

## MYSQL

**Server Installation**
```
sudo apt install -f mysql-server
sudo apt-get install -y mysql-server mysql-client
sudo service mysql status 
sudo service mysql restart
sudo mysql 
    FLUSH PRIVILEGES;
    ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';
    GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;
    SHOW GLOBAL VARIABLES LIKE 'PORT';
sudo mysql -u root -p
```

[ERROR 1698 (28000): Access denied for user 'root'@'localhost'](https://stackoverflow.com/questions/39281594/error-1698-28000-access-denied-for-user-rootlocalhost)
- https://stackoverflow.com/questions/34627533/how-to-check-logs-in-mysql-workbench

CREATE USER 'lrngsql'@'localhost' IDENTIFIED BY 'xyz'
GRANT ALL PRIVILEGES ON bank.* TO 'lrngsql'@'localhost' WITH GRANT OPTION;;

**Workbench UI**

Download the DEB package from : https://dev.mysql.com/downloads/workbench/
```
sudo dpkg -i mysql-workbench-community-dbgsym_8.0.24-1ubuntu20.04_amd64.deb
sudo apt --fix-broken install 
```