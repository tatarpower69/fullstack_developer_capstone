"""Capture actual cURL output without publishing passwords or session cookies."""
import http.cookiejar
import json
import os
import shlex
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
out=ROOT/'evidence'
private=out/'private'
private.mkdir(parents=True,exist_ok=True)
base=os.environ.get('APP_URL','http://127.0.0.1:8000').rstrip('/')
curl='curl.exe' if os.name=='nt' else 'curl'
cookie=str(private/'cookies.txt')
def run(args):
    result=subprocess.run([curl,'--silent','--show-error','--fail-with-body','--max-time','20',*args],capture_output=True,text=True,check=True)
    return result.stdout
def record(name,args):
    result=run(args)
    command=' '.join(shlex.quote(x) for x in [curl,*args]).replace(str(ROOT)+os.sep,'')
    (out/name).write_text('$ '+command+'\n'+result+'\n',encoding='utf-8')
    print(name+': captured',flush=True)
    return result
for name,path in [('getdealerreviews','/djangoapp/reviews/dealer/1'),('getalldealers','/djangoapp/get_dealers'),('getdealerbyid','/djangoapp/dealer/1'),('getdealersbyState','/djangoapp/get_dealers/Kansas'),('getallcarmakes','/djangoapp/get_cars'),('analyzereview','/djangoapp/analyze_review?text=Fantastic%20services')]:
    record(name,[base+path])
accounts=json.loads((private/'accounts.json').read_text())
login_path=private/'login.json'
login_path.write_text(json.dumps({'userName':'capstone_driver','password':accounts['capstone_driver']}))
def post(name,path,datafile):
    run(['-c',cookie,'-b',cookie,base+'/djangoapp/csrf'])
    jar=http.cookiejar.MozillaCookieJar(cookie);jar.load(ignore_discard=True,ignore_expires=True)
    token=next(c.value for c in jar if c.name=='csrftoken')
    # A CSRF token is not a login secret; cookies and passwords stay in ignored files.
    return record(name,['-X','POST','-c',cookie,'-b',cookie,'-H','Content-Type: application/json','-H','X-CSRFToken: '+token,'--data-binary',datafile.read_text(),base+path])
post('loginuser','/djangoapp/login',login_path)
empty=private/'empty.json';empty.write_text('{}')
post('logoutuser','/djangoapp/logout',empty)
