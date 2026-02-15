"""
Gunicorn configuration file
Optimized for Termux environment
"""

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
# For Termux, use fewer workers to save memory
workers = 2  # Reduced for Termux (normally: multiprocessing.cpu_count() * 2 + 1)
worker_class = "sync"
worker_connections = 1000
max_requests = 1000  # Restart workers after handling this many requests
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Server mechanics
daemon = False  # Don't daemonize (run in foreground)
pidfile = None
user = None
group = None
tmp_upload_dir = None

# Logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "absensi-web"

# Server hooks
def on_starting(server):
    """Create logs directory if it doesn't exist"""
    if not os.path.exists('logs'):
        os.makedirs('logs')

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def on_reload(server):
    server.log.info("Server reloaded")

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
