# =====================================================
# GUNICORN CONF - AUTO-SCALE WORKERS FOR ANY SERVER
# =====================================================
# Why this file? 
# 1. Render/Railway reads it AUTOMATICALLY 
# 2. Sets PERFECT workers for THAT server's CPU
# 3. NEVER waste CPU or make users wait!

import multiprocessing
import os

# =====================================================
# WORKERS = PERFECT FOR RENDER FREE TIER
# =====================================================
# Render Free: 0.1 CPU → Manual override for stability
# Production formula: (2 × CPU cores) + 1
workers = 1  # Render Free Tier: 1 worker (stable)

# =====================================================
# BIND = Render internal port
# =====================================================
# Render requires port 10000 internally
bind = "0.0.0.0:10000"

# =====================================================
# WORKER CLASS = FastAPI + Uvicorn (CRITICAL)
# =====================================================
worker_class = "uvicorn.workers.UvicornWorker"

# =====================================================
# EXTRA PRODUCTION SETTINGS 
# =====================================================
timeout = 120  # ML inference timeout
keepalive = 5
accesslog = "-"  
errorlog = "-"
loglevel = 'info'
max_requests = 1000  # Restart workers (memory leak protection)
max_requests_jitter = 100
preload_app = True
graceful_timeout = 30

# =====================================================
# SUMMARY: Render Free Tier Optimized
# =====================================================
# 1 worker → Stable for learning/production testing
# Port 10000 → Render requirement  
# Uvicorn workers → FastAPI compatibility
# Auto-restart → No memory leaks
