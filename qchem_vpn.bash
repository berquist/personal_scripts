#!/usr/bin/env bash

sudo nmcli --ask connection up Q-Chem
sudo ip route add 192.168.0.0/24 dev ppp0
