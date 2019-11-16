sleep 15
touch /var/run/shutdown_signal/signal
echo "waiting" > /var/run/shutdown_signal/signal
while inotifywait -e close_write /var/run/shutdown_signal/signal; do 
  signal=$(cat /var/run/shutdown_signal/signal)
  if [ "$signal" == "shutdown" ]; then 
    echo "done" > /var/run/shutdown_signal/signal
    sudo shutdown -h now
  elif [ "$signal" == "restart" ]; then
  	echo "done" > /var/run/shutdown_signal/signal
  	sudo shutdown -r now
  fi
done