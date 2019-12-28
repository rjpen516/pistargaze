sleep 30
touch /var/run/videostream/signal
echo "waiting" > /var/run/videostream/signal
while inotifywait -e close_write /var/run/videostream/signal; do 
  signal=$(cat /var/run/videostream/signal | head -1)
  if [ "$signal" == "stream" ]; then 
    echo "done" > /var/run/videostream/signal
    gphoto2 --capture-movie --stdout | /opt/ffmpeg -i pipe:0 http://localhost:8090/feed1.ffm & 
  elif [ "$signal" == "stopstream" ]; then
  	echo "done" > /var/run/videostream/signal
  	kill -9 `ps aux  | grep gphoto2 | awk '{print $2}'`
  elif [ "$signal" == "iso" ]; then
  	config=$(sed '2q;d' /var/run/videostream/signal)
  	gphoto2 --auto-detect --set-config=/main/imgsettings/iso=$config
  	echo "done" > /var/run/videostream/signal
  elif [ "$signal" == "shutterspeed" ]; then
  	config=$(sed '2q;d' /var/run/videostream/signal)
  	gphoto2 --auto-detect --set-config=/main/capturesettings/shutterspeed=$config
  	echo "done" > /var/run/videostream/signal
  elif [ "$signal" == "imageformat" ]; then
  	config=$(sed '2q;d' /var/run/videostream/signal)
  	gphoto2 --auto-detect --set-config=/main/imgsettings/imageformat=$config
  	echo "done" > /var/run/videostream/signal
  elif [ "$signal" == "capture" ]; then
  	config=$(sed '2q;d' /var/run/videostream/signal)
  	filename=$(gphoto2 --auto-detect -B $config --capture-image-and-download | grep -ri "Saving file as " | cut -d" " -f 4)
  	echo "$filename" > /var/run/videostream/signal
  elif [ "$signal" == "status" ]; then 
  	ps aux  | grep "gphoto2 --capture-movie --stdout" | grep -v "grep" | awk '{print $2}' > /var/run/videostream/signal
  fi
done



#--capture-image-and-download
#--capture-image
#/main/imgsettings/iso
#/main/imgsettings/imageformat
#/main/status/batterylevel
#/main/capturesettings/shutterspeed