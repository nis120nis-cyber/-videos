#!/bin/bash
# מייצר את סרטון האתגר היומי: ./make.sh  -> final.mp4 + info.txt (ומוסיף שורה ל-done.txt)
set -e; cd "$(dirname "$0")"
read ID N NAME CAP CONT <<< "$(node pick.js)"; NAME=${NAME//_/ }; CAP=${CAP//_/ }
DATE=$(TZ=Asia/Jerusalem date +%d.%m.%Y)
echo "picked: $ID #$N $NAME / $CAP / $CONT"
python3 sfx.py
python3 vo.py "$NAME" "$CAP" "$CONT"
node render.js "$ID" "$N" "$DATE" quiz.mp4
ffmpeg -y -loglevel error -i quiz.video.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -shortest final.mp4
echo "$N $ID $NAME $(TZ=Asia/Jerusalem date +%F)" >> done.txt
printf 'ID=%s\nN=%s\nNAME=%s\nCAP=%s\nCONT=%s\n' "$ID" "$N" "$NAME" "$CAP" "$CONT" > info.txt
echo DONE
