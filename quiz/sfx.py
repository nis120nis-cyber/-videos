# יוצר פסקול: צליל פתיחה, טיק בכל שנייה בספירה, צלצול בחשיפה, אקורד בסיום
import numpy as np, wave
SR=44100; DUR=23
a=np.zeros(int(SR*DUR))
def tone(t0,f,d,v=.3,decay=8,harm=(1,.3,.12)):
    n=int(SR*d); x=np.arange(n)/SR; env=np.exp(-decay*x)*np.minimum(1,x*200)
    s=sum(h*np.sin(2*np.pi*f*(i+1)*x) for i,h in enumerate(harm))*env*v
    i=int(SR*t0); a[i:i+n]+=s[:len(a)-i]
# פתיחה: שני צלילים רכים
tone(0.15,523.25,1.2,.18,3); tone(0.35,783.99,1.4,.14,3)
# מעבר למדינה: "שוש" רך
n=int(SR*1.6); x=np.arange(n)/SR; noise=np.random.default_rng(1).normal(0,1,n)
env=np.sin(np.pi*x/1.6)**2*.05; i=int(SR*3.0); a[i:i+n]+=np.convolve(noise,np.ones(30)/30,'same')*env
# המדינה נדלקת
tone(4.8,659.25,.8,.16,5)
# ספירה 5..1: טיק, שני האחרונים גבוהים יותר
for k,t in enumerate([6.6,7.6,8.6,9.6,10.6]):
    tone(t,1400 if k<3 else 1760,.09,.22,40,(1,.2))
# חשיפה: אקורד מז'ורי
for f,dl in [(523.25,0),(659.25,.06),(783.99,.12),(1046.5,.18)]: tone(12.6+dl,f,1.6,.16,2.5)
# סיום
tone(16.6,392,1.2,.12,3); tone(16.75,523.25,1.4,.12,3)
a=a/np.max(np.abs(a))*.85
w=wave.open('sfx.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((a*32767).astype(np.int16).tobytes()); w.close()
print('ok')
