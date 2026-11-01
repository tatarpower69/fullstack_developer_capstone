"""Run all three application services; terminate them together with Ctrl+C."""
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
processes=[]
try:
    for command, cwd in [(['node','index.js'], ROOT/'services/dealers'),([sys.executable,'app.py'],ROOT/'services/sentiment'),([sys.executable,'manage.py','runserver','127.0.0.1:8000','--noreload'],ROOT/'server')]:
        processes.append(subprocess.Popen(command,cwd=cwd))
    print('Open http://127.0.0.1:8000 — Ctrl+C stops all services',flush=True)
    while all(p.poll() is None for p in processes): time.sleep(1)
finally:
    for process in processes:
        if process.poll() is None: process.terminate()
    for process in processes: process.wait(timeout=15)
