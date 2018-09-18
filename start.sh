uwsgi --http :5000 --gevent 1000 --http-websockets --master --wsgi-file server.py --callable app --disable-logging --py-autoreload 1 
