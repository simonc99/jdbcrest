bind = "127.0.0.1:8000"

workers = 4

worker_class = "sync"

timeout = 30

keepalive = 5

max_requests = 1000

max_requests_jitter = 50

accesslog = "/var/log/jdbc-api/access.log"

errorlog = "/var/log/jdbc-api/error.log"
