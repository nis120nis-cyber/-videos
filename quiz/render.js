// שימוש: node render.js <מזהה מדינה> <מספר אתגר> "<תאריך>" <קובץ יציאה>
const p=require('puppeteer-core');const {spawn}=require('child_process');const fs=require('fs');
const [id,n,date,out]=[process.argv[2]||"392",+process.argv[3]||1,process.argv[4]||"",process.argv[5]||"quiz.mp4"];
(async()=>{
  const b=await p.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox','--allow-file-access-from-files']});const pg=await b.newPage();
  await pg.setViewport({width:1080,height:1920});await pg.goto('file://'+__dirname+'/video.html'+(process.env.THEME=='dark'?'#dark':''));
  const info=await pg.evaluate((id,n,date)=>setup(id,{n,date}),id,n,date);
  const DUR=await pg.evaluate(()=>DUR), FPS=30, N=DUR*FPS, tmp=out.replace(/\.mp4$/,'')+'.part.mp4';
  const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',tmp],{stdio:['pipe','inherit','inherit']});
  for(let i=0;i<N;i++){ const d=await pg.evaluate(t=>grab(t,.92),i/FPS); if(!ff.stdin.write(Buffer.from(d.split(',')[1],'base64'))) await new Promise(r=>ff.stdin.once('drain',r)); }
  ff.stdin.end(); const code=await new Promise(r=>ff.on('close',r)); await b.close();
  if(code!==0) throw new Error('ffmpeg failed');
  fs.renameSync(tmp,out.replace(/\.mp4$/,'')+'.video.mp4'); console.log(JSON.stringify(info));
})();
