// בוחר את המדינה הבאה שעוד לא הופיעה (קודם מוכרות, רמה 0-2, ואז השאר). פלט: id n name cap cont
global.window=global; const fs=require('fs');
eval(fs.readFileSync(__dirname+'/data.js','utf8').replace(/^const /gm,'var '));
const f=__dirname+'/done.txt', done=fs.existsSync(f)?fs.readFileSync(f,'utf8').split('\n').filter(l=>l.trim()&&!l.startsWith('#')):[];
const used=new Set(done.map(l=>l.split(' ')[1]));
let pool=Object.keys(META).filter(k=>!used.has(k)&&META[k][3]<=2&&FLAGS[k]);
if(!pool.length) pool=Object.keys(META).filter(k=>!used.has(k)&&FLAGS[k]);
if(!pool.length) pool=Object.keys(META).filter(k=>FLAGS[k]);
const id=pool[Math.floor(Math.random()*pool.length)], m=META[id];
console.log([id, done.length+1, m[0].replace(/ /g,'_'), m[1].replace(/ /g,'_'), m[2]].join(' '));
