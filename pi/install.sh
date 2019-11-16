#!/bin/bash

apt-get update
apt-get install -y libffi-dev inotify-tools

sudo apt-get install apt-transport-https ca-certificates software-properties-common -y
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
sudo usermod -aG docker pi
echo "deb https://download.docker.com/linux/raspbian/ stretch stable" >> vim /etc/apt/sources.list


sudo apt-get upgrade


systemctl start docker.service


sudo apt install docker-ce docker-compose