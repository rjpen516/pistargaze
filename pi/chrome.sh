#!/bin/sh
DISPLAY=:0
xset -dpms
xset s off
xset s noblank

unclutter &
chromium-browser https://google.com --start-fullscreen --kiosk --incognito --noerrdialogs --disable-translate --no-first-run --fast --fast-start --disable-infobars --disable-features=TranslateUI --disk-cache-dir=/dev/null  --password-store=basic