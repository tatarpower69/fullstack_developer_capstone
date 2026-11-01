import React, {useState} from 'react';
import {api} from '../../api';

export default function Register({onLogin}) {
  const [error,setError]=useState('');const [busy,setBusy]=useState(false);
  async function submit(event) {
    event.preventDefault();setBusy(true);setError('');
    try {const result=await api('registration',Object.fromEntries(new FormData(event.currentTarget)));onLogin(result.user);}
    catch(e){setError(e.message);}finally{setBusy(false);}
  }
  return <section className="auth card"><p className="eyebrow">YOUR NEXT CHAPTER</p><h1>Create your account</h1><p className="muted">Join the conversation. Share your experience.</p><form onSubmit={submit}>
    <label>Username<input name="username" required autoComplete="username" maxLength="150" /></label>
    <div className="two"><label>First Name<input name="first_name" required autoComplete="given-name" /></label><label>Last Name<input name="last_name" required autoComplete="family-name" /></label></div>
    <label>Email<input name="email" type="email" required autoComplete="email" /></label>
    <label>Password<input name="password" type="password" required minLength="8" autoComplete="new-password" /></label>
    {error&&<p role="alert" className="error">{error}</p>}<button className="primary" disabled={busy}>{busy?'Creating account…':'Register'}</button>
  </form><p>Already a member? <a href="/login">Sign in</a></p></section>;
}
