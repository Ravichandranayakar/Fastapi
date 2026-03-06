# =====================================================
# GUNICORN CONF - AUTO-SCALE WORKERS FOR ANY SERVER
# =====================================================
# Why this file? 
# 1. Render/Railway reads it AUTOMATICALLY 
# 2. Sets PERFECT workers for THAT server's CPU
# 3. NEVER waste CPU or make users wait!
# 

import multiprocessing  #  Python's CPU counter
import os               #  Environment variables (Render sets these)

# =====================================================
# WORKERS = MAGIC FORMULA 
# =====================================================
# Formula: (2 × CPU cores) + 1 = PERFECT workers
# 
# laptop: 4 cores → 2×4 +1 = 9 workers
# Render basic: 2 cores → 2×2 +1 = 5 workers  
# Render pro: 8 cores → 2×8 +1 = 17 workers
#
workers = multiprocessing.cpu_count() * 2 + 1

# What happens:
# multiprocessing.cpu_count() → Counts YOUR CPU cores (4, 8, 16...)
# * 2 → Double it (each core handles 2 requests)
# + 1 → Extra worker for smooth handoffs
# Result → Printed in logs: "Starting 9 workers"

# =====================================================
# BIND = Where Gunicorn listens
# =====================================================
# "0.0.0.0:8000" = Listen on ALL network interfaces, port 8000
# Why 0.0.0.0? Docker/Render needs this (not 127.0.0.1)
bind = "0.0.0.0:8000"  

# =====================================================
# WORKER CLASS = FastAPI needs Uvicorn inside Gunicorn
# =====================================================
# FastAPI = ASGI framework → needs Uvicorn workers
# Gunicorn alone = WSGI → can't run FastAPI!
#
# "uvicorn.workers.UvicornWorker" = Gunicorn runs Uvicorn clones
worker_class = "uvicorn.workers.UvicornWorker"

# =====================================================
# EXTRA PRODUCTION SETTINGS 
# =====================================================
# How long worker waits for slow request (30 sec)
timeout = 30

# Keep-alive for multiple requests (improves speed)
keepalive = 5

# Log where? (Render reads these)
accesslog = "-"   # Log to stdout (Docker logs)
errorlog = "-"    # Error log to stdout

# Graceful restart (zero downtime deploys)
graceful_timeout = 30

# =====================================================
# SUMMARY: What this does for 10M users?
# =====================================================
# 1. Laptop → 9 workers (handles 1000s req/sec)
# 2. Render detects CPU → sets perfect workers
# 3. 100K users? → Render adds 10 servers (90 workers total)
# 4. 10M users? → Render adds 1000 servers (9000 workers)

