#!/bin/bash

mkdir /data

cp -R ../../pistargaze /data/

apt-get update
apt-get install -y libffi-dev inotify-tools screen python-gps

sudo apt-get install apt-transport-https ca-certificates software-properties-common -y
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
sudo usermod -aG docker pi
echo "deb https://download.docker.com/linux/raspbian/ stretch stable" >> vim /etc/apt/sources.list


sudo apt-get upgrade -y


systemctl start docker.service


sudo apt install docker-ce docker-compose -y

sudo cp /data/pistargaze/pi/gphoto.service /etc/systemd/system/gphoto.service
sudo cp /data/pistargaze/pi/shutdown.service /etc/systemd/system/shutdown.service
sudo systemctl enable gphoto
sudo systemctl start gphoto

sudo systemctl enable shutdown
sudo systemctl start shutdown


sudo apt-get install unclutter

