cp ../.env .

export $(grep -v '^#' .env | xargs)

db_port=$DB_PORT
db_name=$DB_NAME
db_user=$DB_USER
db_pass=$DB_PASSWORD

chmod 600 .env

PGPASSWORD=$db_pass psql -h localhost -U $db_user -d $db_name -p $db_port < init_bd.sql
PGPASSWORD=$db_pass psql -h localhost -U $db_user -d $db_name -p $db_port < populate.sql
