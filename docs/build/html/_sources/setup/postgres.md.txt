# PostgreSQL

Home url : [https://www.postgresql.org/](https://www.postgresql.org/)  
Here is a good comparision [PostgreSQL vs MySQL](https://www.postgresqltutorial.com/postgresql-vs-mysql/)   
 
## Setup

**1. Manual**

```
#install ubuntu packages
sudo apt-get install postgresql postgresql-contrib

# check the version
sudo -u postgres psql -c "SELECT version();"

# test the installation
sudo su - postgres
    psql #to launch the terminal
    \q #to quit

# or to run psql directly
sudo -i -u postgres psql

```

To cut short the permission configurations for new users, lets create an Ubuntu user with same name: 
`sudo adduser mozhi #password mozhi` 

We need log into PostgresSQL to create users before they can use the DB.
For our case we are going ot create a user called `mozhi` and DB called `mozhidb`

```
sudo su - postgres
    psql #to launch the terminal
    # drop user mozhi;
    CREATE USER mozhi WITH PASSWORD 'mozhi'; 
    \du #list users
    CREATE DATABASE mozhidb;
    grant all privileges on database mozhidb to mozhi;
    ALTER USER mozhi WITH CREATEDB;
    \list # to see the DB created
    \q

# test the new user and DB
sudo -i -u mozhi  psql -d mozhidb
    CREATE TABLE corpus (id int NOT NULL, text TEXT NOT NULL, PRIMARY KEY (id));
    INSERT INTO corpus VALUES(1,'Ravi is sales person from 2012-08-15');
    INSERT INTO corpus VALUES(2,'Kumar is sales person from 2012-09-15');
    INSERT INTO corpus VALUES(3,'Sathis is sales person from 2012-10-15');
    \dt #list tables
    \conninfo #get connection info
```

Fire a python shell and test out the connection

```  
import pandas as pd  
import psycopg2
conn = psycopg2.connect(host="localhost", port=5432, database="mozhidb", user="mozhi", password="mozhi")
sql_command = "SELECT * FROM \"corpus\";"
print (sql_command)
# Load the data
data = pd.read_sql(sql_command, conn)
print(data)
```

**2. Docker**

[Reference](https://towardsdatascience.com/local-development-set-up-of-postgresql-with-docker-c022632f13ea)

```bash
# Postgresql Environment variables
# https://github.com/docker-library/docs/blob/master/postgres/README.md
    POSTGRES_PASSWORD
    POSTGRES_USER
    PGDATA
    POSTGRES_DB
    POSTGRES_INITDB_ARGS
```

```
docker pull postgres
mkdir -p ${HOME}/.mozhi/postgres-data/

docker run -d \
	--name mozhi-db-server-test \
	-e POSTGRES_USER=mozhi \
	-e POSTGRES_PASSWORD=mozhi \
	-v ${HOME}/postgres-data/:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres

psql -h localhost -U mozhi # pass: mozhi     

psql -h mypostgres -U postgres # pass: mozhi     


# clear docker volume data if needed
sudo rm -rf ${HOME}/postgres-data/ 
```

**3. Kubernetes**

```
cd /path/to/mozhi/
kubectl apply -f ops/k8s/services/postgresql-configmap.yaml
kubectl apply -f ops/k8s/services/postgresql.yaml

kubectl apply -f ops/k8s/services/namespace.yaml
kubectl apply -f https://raw.githubusercontent.com/reactive-tech/kubegres/v1.7/kubegres.yaml
kubectl apply -f ops/k8s/postgres/mozhi-postgres-secret.yaml 
kubectl apply -f ops/k8s/postgres/mozhi-postgres.yaml
kubectl get pod,statefulset,svc,configmap -o wide -n mozhi
 
# test the service
kubectl exec -it service/mozhi-postgres-db -n mozhi -- bash
 >> psql -U postgres
 >> mozhi
 
 
kubectl -n mozhi port-forward service/mozhi-postgres-db 4321:5432

psql -h localhost -U postgres
>>mozhi
```


## Misc
- To know the file storage in Postgres, this is to make sure the data in Docker can be mapped to a volume for offline storage.

`SELECT name, setting FROM pg_settings WHERE category = 'File Locations';`

- If you would like to restart the service:

```
sudo service postgresql restart
sudo systemctl restart postgresql
```

- To see how many active connections to the DB are made:
`SELECT pid, application_name, state FROM pg_stat_activity;`
This is important some times the connetion becomes stale and left hanging there, making new connection bounce back.

- Service management commands:

```
sudo service postgresql stop
sudo service postgresql start
sudo service postgresql restart
```

- To delete all tables 

```
SELECT
  'DROP TABLE IF EXISTS "' || tablename || '" CASCADE;' 
from
  pg_tables WHERE schemaname = 'public';
```

------------------------------------------------------------------------------------------------------------------------

## PSQL

Magic words:
```bash
psql -U postgres
```
Some interesting flags (to see all, use `-h` or `--help` depending on your psql version):
- `-E`: will describe the underlaying queries of the `\` commands (cool for learning!)
- `-l`: psql will list all databases and then exit (useful if the user you connect with doesn't has a default database, like at AWS RDS)

Most `\d` commands support additional param of `__schema__.name__` and accept wildcards like `*.*`

- `\q`: Quit/Exit
- `\c __database__`: Connect to a database
- `\d __table__`: Show table definition including triggers
- `\d+ __table__`: More detailed table definition including description and physical disk size
- `\l`: List databases
- `\dy`: List events
- `\df`: List functions
- `\di`: List indexes
- `\dn`: List schemas
- `\dt *.*`: List tables from all schemas (if `*.*` is omitted will only show SEARCH_PATH ones)
- `\dT+`: List all data types
- `\dv`: List views
- `\df+ __function__` : Show function SQL code. 
- `\x`: Pretty-format query results instead of the not-so-useful ASCII tables
- `\copy (SELECT * FROM __table_name__) TO 'file_path_and_name.csv' WITH CSV`: Export a table as CSV

User Related:
- `\du`: List users
- `\du __username__`: List a username if present.
- `create role __test1__`: Create a role with an existing username.
- `create role __test2__ noinherit login password __passsword__;`: Create a role with username and password.
- `set role __test__;`: Change role for current session to `__test__`.
- `grant __test2__ to __test1__;`: Allow `__test1__` to set its role as `__test2__`.

Drop all the tables in a database:
```
DROP SCHEMA public CASCADE;
CREATE SCHEMA public AUTHORIZATION {USER};
GRANT ALL ON schema public TO {USER};
```

## Configuration

- Changing verbosity & querying Postgres log:
  <br/>1) First edit the config file, set a decent verbosity, save and restart postgres:
```
sudo vim /etc/postgresql/9.3/main/postgresql.conf

# Uncomment/Change inside:
log_min_messages = debug5
log_min_error_statement = debug5
log_min_duration_statement = -1

sudo service postgresql restart
```
  2) Now you will get tons of details of every statement, error, and even background tasks like VACUUMs
```
tail -f /var/log/postgresql/postgresql-9.3-main.log
```
  3) How to add user who executed a PG statement to log (editing `postgresql.conf`):
```
log_line_prefix = '%t %u %d %a '
```

## Create command

There are many `CREATE` choices, like `CREATE DATABASE __database_name__`, `CREATE TABLE __table_name__` ... Parameters differ but can be checked [at the official documentation](https://www.postgresql.org/search/?u=%2Fdocs%2F9.1%2F&q=CREATE).


## Handy queries
- `SELECT * FROM pg_proc WHERE proname='__procedurename__'`: List procedure/function
- `SELECT * FROM pg_views WHERE viewname='__viewname__';`: List view (including the definition)
- `SELECT pg_size_pretty(pg_total_relation_size('__table_name__'));`: Show DB table space in use
- `SELECT pg_size_pretty(pg_database_size('__database_name__'));`: Show DB space in use
- `show statement_timeout;`: Show current user's statement timeout
- `SELECT * FROM pg_indexes WHERE tablename='__table_name__' AND schemaname='__schema_name__';`: Show table indexes
- Get all indexes from all tables of a schema:
```sql
SELECT
   t.relname AS table_name,
   i.relname AS index_name,
   a.attname AS column_name
FROM
   pg_class t,
   pg_class i,
   pg_index ix,
   pg_attribute a,
    pg_namespace n
WHERE
   t.oid = ix.indrelid
   AND i.oid = ix.indexrelid
   AND a.attrelid = t.oid
   AND a.attnum = ANY(ix.indkey)
   AND t.relnamespace = n.oid
    AND n.nspname = 'kartones'
ORDER BY
   t.relname,
   i.relname
```
- Execution data:
  - Queries being executed at a certain DB:
```sql
SELECT datname, application_name, pid, backend_start, query_start, state_change, state, query 
  FROM pg_stat_activity 
  WHERE datname='__database_name__';
```
  - Get all queries from all dbs waiting for data (might be hung): 
```sql
SELECT * FROM pg_stat_activity WHERE waiting='t'
```
  - Currently running queries with process pid:
```sql
SELECT pg_stat_get_backend_pid(s.backendid) AS procpid, 
  pg_stat_get_backend_activity(s.backendid) AS current_query
FROM (SELECT pg_stat_get_backend_idset() AS backendid) AS s;
```

Casting:
- `CAST (column AS type)` or `column::type`
- `'__table_name__'::regclass::oid`: Get oid having a table name

Query analysis:
- `EXPLAIN __query__`: see the query plan for the given query
- `EXPLAIN ANALYZE __query__`: see and query_to_df the query plan for the given query
- `ANALYZE [__table__]`: collect statistics  

Generating random data ([source](https://www.citusdata.com/blog/2019/07/17/postgres-tips-for-average-and-power-user/)):
- `INSERT INTO some_table (a_float_value) SELECT random() * 100000 FROM generate_series(1, 1000000) i;`

Keyboard shortcuts
- `CTRL` + `R`: reverse-i-search



**References**

- https://www.tecmint.com/install-postgresql-on-ubuntu/
- https://linuxize.com/post/how-to-install-postgresql-on-ubuntu-18-04/
- https://medium.com/@thomaspt748/how-to-upsert-data-into-relational-database-using-spark-7d2d92e05bb9
- https://linuxize.com/post/how-to-create-a-sudo-user-on-ubuntu/
- https://stackoverflow.com/questions/21898152/why-cant-you-start-postgres-in-docker-using-service-postgres-start
- https://markheath.net/post/exploring-postgresql-with-docker
- `ptop` and `pg_top`: `top` for PG. Available on the APT repository from `apt.postgresql.org`.
- [pg_activity](https://github.com/julmon/pg_activity): Command line tool for PostgreSQL server activity monitoring.
- [Unix-like reverse search in psql](https://dba.stackexchange.com/questions/63453/is-there-a-psql-equivalent-of-bashs-reverse-search-history):
```bash
$ echo "bind "^R" em-inc-search-prev" > $HOME/.editrc
$ source $HOME/.editrc
``` 
- [PostgreSQL Exercises](https://pgexercises.com/): An awesome resource to learn to learn SQL, teaching you with simple examples in a great visual way. **Highly recommended**.
- [A Performance Cheat Sheet for PostgreSQL](https://severalnines.com/blog/performance-cheat-sheet-postgresql): Great explanations of `EXPLAIN`, `EXPLAIN ANALYZE`, `VACUUM`, configuration parameters and more. Quite interesting if you need to tune-up a postgres setup.





