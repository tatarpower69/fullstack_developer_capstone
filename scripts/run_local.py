"""Run all three application services; terminate them together with Ctrl+C."""
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
processes=[]
web_port=os.environ.get('WEB_PORT','8000')
dealer_port=os.environ.get('DEALER_PORT','3030')
sentiment_port=os.environ.get('SENTIMENT_PORT','5050')
os.environ['PORT']=dealer_port
os.environ['DEALERS_URL']='http://127.0.0.1:'+dealer_port
os.environ['SENTIMENT_URL']='http://127.0.0.1:'+sentiment_port
try:
    for command, cwd in [(['node','index.js'], ROOT/'services/dealers'),([sys.executable,'-u','app.py'],ROOT/'services/sentiment'),([sys.executable,'-u','manage.py','runserver','127.0.0.1:'+web_port,'--noreload'],ROOT/'server')]:
        processes.append(subprocess.Popen(command,cwd=cwd))
    print('Open http://127.0.0.1:'+web_port+' — Ctrl+C stops all services',flush=True)
    while all(p.poll() is None for p in processes): time.sleep(1)
finally:
    for process in processes:
        if process.poll() is None: process.terminate()
    for process in processes: process.wait(timeout=15)
