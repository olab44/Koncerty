# db_pass=$1
# export PGPASSWORD=db_pass
# echo $PGPASSWORD
chmod 0600 .pgpass
cp .pgpass ~/
psql -h localhost -U postgres -d koncerty_db -p 5432 < init_bd.sql 
psql -h localhost -U postgres -d koncerty_db -p 5432 < populate.sql 
