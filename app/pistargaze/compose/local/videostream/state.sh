sleep 30
touch /var/run/videostream/signal
echo "waiting" > /var/run/videostream/signal
while inotifywait -e close_write /var/run/videostream/signal; do 
  signal=$(cat /var/run/videostream/signal)
  if [ "$signal" == "stream" ]; then 
    echo "done" > /var/run/videostream/signal
    gphoto2 --capture-movie --stdout | /opt/ffmpeg -i pipe:0 http://localhost:8090/feed1.ffm & 
  elif [ "$signal" == "stopstream" ]; then
  	echo "done" > /var/run/videostream/signal
  	kill -9 `ps aux  | grep gphoto2 | cut -d$' ' -f 8`
  fi
done