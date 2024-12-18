db_port=$1
db_name=$2
db_user=$3
db_pass=$4  
# chmod 0600 .pgpass
# cp .pgpass ~/
PGPASSWORD=$db_pass psql -h localhost -U $db_user -d $db_name -p $db_port < init_bd.sql 
PGPASSWORD=$db_pass psql -h localhost -U $db_user -d $db_name -p $db_port < populate.sql 
