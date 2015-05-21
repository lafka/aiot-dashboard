apt-get update
apt-get install -y python-dev ruby python-pip libffi-dev bcrypt
gem install sass

pip install virtualenv

su - vagrant -c "virtualenv /home/vagrant/djenv"
echo "source /home/vagrant/djenv/bin/activate" >/home/vagrant/.bashrc

su - vagrant -c "pip install -r /home/vagrant/aiot/requirements/dev.txt"

# Postgres
apt-get install -y libpq-dev
pip install psycopg2==2.5.4
su - vagrant -c "pip install psycopg2==2.5.4"
apt-get -y install postgresql-9.3
su -c "createuser -s -w aiot" -m "postgres"
su -c "psql -c \"ALTER USER aiot WITH PASSWORD 'aiot';\"" -m "postgres"
echo "host  all     all     127.0.0.1/32        password" >> /etc/postgresql/9.3/main/pg_hba.conf

/etc/init.d/postgresql restart

su -c "psql -c \"CREATE DATABASE aiot;\"" -m "postgres"
su -c "psql -d aiot </home/vagrant/aiot/conf/vagrant/schema.sql" -m "postgres"

su - vagrant -c "cd aiot; ./manage.py migrate"


# UWSGI
su - vagrant -c "pip install uwsgi gevent"

echo "start on vagrant-mounted
stop on shutdown

script
su - vagrant -c \"cd /home/vagrant/aiot/; exec uwsgi --http :8000 --async 100 --ugreen --module core.wsgi --py-autoreload=3\"
end script" > /etc/init/django.conf

initctl start django
