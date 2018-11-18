import multiprocessing

bind = '0.0.0.0:8443'
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = '/home/jcb/etc/gunicorn_access_log'
