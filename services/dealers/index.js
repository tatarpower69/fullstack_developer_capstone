import http from 'node:http';
import { readFile, writeFile, rename } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { timingSafeEqual } from 'node:crypto';

const seed = JSON.parse(await readFile(new URL('./seed.json', import.meta.url), 'utf8'));
let db, client, data;
const runtime = fileURLToPath(new URL('./runtime.json', import.meta.url));
if (process.env.MONGO_URL) {
  const { MongoClient } = await import('mongodb');
  client = new MongoClient(process.env.MONGO_URL);
  await client.connect(); db = client.db('dealership');
  for (const name of ['dealers', 'reviews']) {
    if (!(await db.collection(name).countDocuments())) await db.collection(name).insertMany(seed[name]);
  }
} else {
  try { data = JSON.parse(await readFile(runtime, 'utf8')); } catch (e) { if(e.code !== 'ENOENT') throw e; data = structuredClone(seed); }
}
const rows = async (name, query={}) => db ? db.collection(name).find(query, {projection:{_id:0}}).toArray() : data[name].filter(row => Object.entries(query).every(([key,value]) => row[key] === value));
let writeQueue = Promise.resolve();
const server = http.createServer(async (req,res) => {
  const reply = (status,body) => {res.writeHead(status, {'Content-Type':'application/json'}); res.end(JSON.stringify(body));};
  try {
    const parts = new URL(req.url,'http://localhost').pathname.split('/').filter(Boolean).map(decodeURIComponent);
    if(req.method === 'GET' && parts[0] === 'health') return reply(200,{status:'ok',storage:db?'mongodb':'development-json'});
    if(req.method === 'GET' && parts[0] === 'fetchDealers') return reply(200,{dealers:await rows('dealers', parts[1]?{state:parts[1]}:{})});
    if(req.method === 'GET' && parts[0] === 'fetchDealer') {
      const dealer = (await rows('dealers',{id:Number(parts[1])}))[0];
      return dealer ? reply(200,{dealer}) : reply(404,{error:'Dealer not found'});
    }
    if(req.method === 'GET' && parts[0] === 'fetchReviews') return reply(200,{reviews:await rows('reviews',{dealership:Number(parts[1])})});
    if(req.method === 'POST' && parts[0] === 'insert_review') {
      const configured = process.env.SERVICE_TOKEN;
      if(configured) {
        const supplied = Buffer.from(req.headers['x-service-token'] || '');
        const expected = Buffer.from(configured);
        if(supplied.length !== expected.length || !timingSafeEqual(supplied,expected)) return reply(403,{error:'Forbidden'});
      }
      let body=''; for await (const chunk of req) { body += chunk; if(body.length>20000) return reply(413,{error:'Payload too large'}); }
      const input=JSON.parse(body);
      if(!(await rows('dealers',{id:Number(input.dealership)})).length) return reply(404,{error:'Dealer not found'});
      if(typeof input.review !== 'string' || !input.review.trim() || input.review.length>5000) return reply(400,{error:'Invalid review'});
      const review={dealership:Number(input.dealership),name:String(input.name||'Customer').slice(0,150),review:input.review,purchase:!!input.purchase,purchase_date:String(input.purchase_date||''),car_make:String(input.car_make||''),car_model:String(input.car_model||''),car_year:Number(input.car_year),sentiment:['positive','negative','neutral'].includes(input.sentiment)?input.sentiment:'neutral'};
      if(db) { await db.collection('reviews').insertOne(review); delete review._id; }
      else {
        const save=async()=>{review.id=Math.max(0,...data.reviews.map(r=>r.id||0))+1;data.reviews.push(review);await writeFile(runtime+'.tmp',JSON.stringify(data,null,2));await rename(runtime+'.tmp',runtime);};
        writeQueue=writeQueue.then(save); await writeQueue;
      }
      return reply(201,{review});
    }
    reply(404,{error:'Not found'});
  } catch(error) {console.error(error.message);reply(500,{error:'Data service error'});}
});
server.listen(Number(process.env.PORT||3030),process.env.BIND_HOST||'127.0.0.1',()=>console.log('Dealership API ready on '+(process.env.PORT||3030)));
process.on('SIGTERM',()=>server.close(async()=>{await client?.close();process.exit(0);}));
