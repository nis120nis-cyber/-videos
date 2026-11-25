# קריינות בעברית (he-IL-HilaNeural) + מיקס עם הצלילים. שימוש: python3 vo.py "<שם>" "<בירה>" <קוד יבשת>
import sys, asyncio, subprocess, json, os
try:  # תעודת הפרוקסי של הסביבה
    import certifi; p=certifi.where(); ca='/root/.ccr/ca-bundle.crt'
    if os.path.exists(ca) and 'CCR_ADDED' not in open(p).read(): open(p,'a').write('\n# CCR_ADDED\n'+open(ca).read())
except Exception as e: print('certifi', e)
import edge_tts
name, cap, cont = sys.argv[1], sys.argv[2], sys.argv[3]
IN = {"AF":"באפריקה","AS":"באסיה","EU":"באירופה","NA":"בצפון או במרכז אמריקה","SA":"בדרום אמריקה","OC":"באוקיאניה"}[cont]
LINES = [  # (זמן התחלה בשניות, טקסט)
  (0.4,  "איזו מדינה זו?"),
  (5.4,  "יש לכם חמש שניות!"),
  (8.9,  f"רמז: היא נמצאת {IN}."),
  (12.7, f"זו {name}! הבירה {cap}."),
  (16.9, "אתגרו חבר בראש בראש. הקישור בביו!"),
]
SLOT_END = [5.3, 8.8, 12.5, 16.8, 22.8]
async def tts(i, text):
    await edge_tts.Communicate(text, "he-IL-HilaNeural", rate="+6%").save(f"vo{i}.mp3")
async def main():
    for i,(t,x) in enumerate(LINES): await tts(i, x)
asyncio.run(main())
dur = lambda f: float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]).decode())
rep=[]
for i,(t,x) in enumerate(LINES):
    d=dur(f"vo{i}.mp3"); rep.append((i,t,round(d,2),round(t+d,2),SLOT_END[i]))
    if t+d>SLOT_END[i]+0.15: print("WARN line",i,"too long",t+d,">",SLOT_END[i])
print(json.dumps(rep))
inputs=["-i","sfx.wav"]+sum([["-i",f"vo{i}.mp3"] for i in range(len(LINES))],[])
fc="[0:a]volume=0.55[s];"+"".join(f"[{i+1}:a]aresample=44100,adelay={int(t*1000)}|{int(t*1000)},volume=1.6[v{i}];" for i,(t,_) in enumerate(LINES))
fc+="[s]"+"".join(f"[v{i}]" for i in range(len(LINES)))+f"amix=inputs={len(LINES)+1}:normalize=0:duration=first,alimiter=limit=0.95[out]"
subprocess.check_call(["ffmpeg","-y","-loglevel","error",*inputs,"-filter_complex",fc,"-map","[out]","-ac","2","-ar","44100","mix.wav"])
print("mix.wav ok")
