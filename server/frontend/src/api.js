export async function api(path, data) {
  const options={credentials:'same-origin',headers:{}};
  if(data !== undefined) {
    const token=await fetch('/djangoapp/csrf',{credentials:'same-origin'}).then(r=>r.json());
    options.method='POST';options.headers={'Content-Type':'application/json','X-CSRFToken':token.csrfToken};options.body=JSON.stringify(data);
  }
  const response=await fetch('/djangoapp/'+path,options);
  const result=await response.json();
  if(!response.ok) throw new Error(result.error||'Unable to complete your request');
  return result;
}
