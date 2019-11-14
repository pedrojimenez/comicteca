#!/bin/sh

#if [ "$DATABASE" = "postgres" ]
#then
#else
echo
echo "-----------------------"
echo "Waiting for $DATABASE ..."
echo "-----------------------"
while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done

echo "$DATABASE started"
# fi

# Flushing Database (dev only)
#echo
#echo "-----------------------"
#echo "Flusing Database" ...
#echo "-----------------------"
#python manage.py flush --noinput

echo
echo "-----------------------"
echo "Migrating Database" ...
echo "-----------------------"
python manage.py migrate

echo
echo "-----------------------"
echo "Collecting Static files"
echo "-----------------------"
python manage.py collectstatic --noinput --clear

exec "$@"
