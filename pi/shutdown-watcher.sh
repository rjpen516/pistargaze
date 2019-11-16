touch /var/run/shutdown_signal/signal
echo "waiting" > /var/run/shutdown_signal/signal
while inotifywait -e close_write /var/run/shutdown_signal/signal; do 
  signal=$(cat /var/run/shutdown_signal/signal)
  if [ "$signal" == "true" ]; then 
    echo "done" > /var/run/shutdown_signal/signal
    shutdown -h now
  fi
done