mysql -u weteam --password=weizoom weteam < rebuild_database.sql
python manage.py syncdb --noinput