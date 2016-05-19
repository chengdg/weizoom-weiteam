mysql -u wemanage --password=weizoom wemanage < rebuild_database.sql
python manage.py syncdb --noinput