set -e

COMICTECA_DB_USER=root
COMICTECA_DB_PASSWORD=temporal
COMICTECA_DJANGO_USER=admin
COMICTECA_DJANGO_PASSWORD=temporal

# nginx server_name
if [ -z "$1" ]; then
    echo "You must supply a 'server_name' argument"
    exit 1
fi
server_name=$1

# number of image's cpu
num_cpus=1
[ -z "$2" ] || num_cpus=$2

# unnatended apt installations
export DEBIAN_FRONTEND=noninteractive
APT_OPTS="-uy -q --force-yes --allow-unauthenticated --no-install-recommends"

apt-mark hold grub-pc

# update system
apt-get update
apt-get upgrade $APT_OPTS

apt-get install git vim htop $APT_OPTS

# install pip
apt-get install python-pip $APT_OPTS
pip install -U pip

# install build project requirements
apt-get install gcc python-dev ldap-utils libldap2-dev libsasl2-dev   \
    libjpeg-dev libmysqlclient-dev $APT_OPTS
pip install -r /vagrant/requirements.txt
# pip install -r /vagrant/requirements-dev.txt

# link to /opt/comicteca
if ! [ -L /opt/comicteca/ ]; then
  rm -rf /opt/comicteca
  ln -fs /vagrant/comicteca /opt/comicteca
fi

# mysql-server
MYSQL_PKG="mysql-server-5.5"
echo "$MYSQL_PKG mysql-server/root_password password ${COMICTECA_DB_PASSWORD}
$MYSQL_PKG mysql-server/root_password seen true
$MYSQL_PKG mysql-server/root_password_again password ${COMICTECA_DB_PASSWORD}
$MYSQL_PKG mysql-server/root_password_again seen true
" | debconf-set-selections
apt-get install $MYSQL_PKG $APT_OPTS
mysql -u root -p$COMICTECA_DB_PASSWORD -e "CREATE DATABASE IF NOT EXISTS comicteca CHARACTER SET utf8;"
mysql -u root -p$COMICTECA_DB_PASSWORD -e "GRANT ALL ON comicteca.* TO '$COMICTECA_DB_USER'@'%' IDENTIFIED BY '$COMICTECA_DB_PASSWORD';"

# log directory
mkdir -p /var/log/comicteca/
chown -R root.vagrant /var/log/comicteca/
chmod 774 /var/log/comicteca/

# setup Comicteca django project
cd /opt/comicteca
python manage.py migrate
### python manage.py collectstatic --noinput

# create superuser
echo "from django.contrib.auth.models import User
if not User.objects.filter(username='$COMICTECA_DJANGO_USER').exists():
    User.objects.create_superuser('$COMICTECA_DJANGO_USER',
                                  'root@localhost',
                                  '$COMICTECA_DJANGO_PASSWORD')" \
| python manage.py shell


##### gunicorn with supervisor ######
pip install gunicorn
apt-get install supervisor $APT_OPTS

# gunicorn workers (2 x $num_cores) + 1
# http://docs.gunicorn.org/en/stable/design.html#how-many-workers
gunicorn_workers=`echo "(2 * $num_cpus) + 1" | bc`

# TODO: move this config file to project/contrib directory
cat > /etc/supervisor/conf.d/comicteca.conf << EOL
[program:comicteca]
command = /usr/bin/python /usr/local/bin/gunicorn
    comicteca.wsgi:application
    --bind=unix:/var/run/comicteca_nginx.sock
    --workers=$gunicorn_workers
directory = /opt/comicteca/
user = root
EOL

supervisorctl reread && supervisorctl update
# TODO: launch on startup
supervisorctl restart comicteca

###### nginx configuration ######
apt-get install nginx $APT_OPTS

# TODO: move this config file to project/contrib directory
cat > /etc/nginx/sites-available/comicteca << EOL
upstream comicteca {
    server unix:/var/run/comicteca_nginx.sock fail_timeout=0;
}
server {
    listen 80;
    server_name $server_name;
    access_log off;
    location /comicteca/static/ {
        alias /opt/comicteca/staticfiles/;
    }
    location /comicteca {
        proxy_pass       http://comicteca;
        proxy_redirect   off;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header SCRIPT_NAME /comicteca;
    }
    location / {
        return 301 /comicteca;
    }
}
EOL

ln -sf /etc/nginx/sites-available/comicteca /etc/nginx/sites-enabled/
service nginx restart

