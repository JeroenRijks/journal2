./manage.py dumpdata > web_data.yaml
./manage.py flush
./manage.py loaddata test_data.yaml
behave
./manage.py flush
./manage.py loaddata web_data.yaml

