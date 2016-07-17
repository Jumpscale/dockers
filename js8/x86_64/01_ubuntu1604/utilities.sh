#!/bin/bash
set -e
source /bd_build/buildconfig
set -x


$minimal_apt_get_install curl less mc rsync sudo tmux lsb-release
$minimal_apt_get_install iproute2 iputils-arping inetutils-telnet inetutils-ftp  inetutils-traceroute 
$minimal_apt_get_install iputils-ping iputils-tracepath iputils-clockdiff

$minimal_apt_get_install python3.5 

$minimal_apt_get_install net-tools

$minimal_apt_get_install git wget 

## This tool runs a command as another user and sets $HOME.
cp /bd_build/bin/setuser /sbin/setuser

#Enable SSHD
rm /etc/service/sshd/down

#Pregenerate the host SSH keys
dpkg-reconfigure openssh-server

#Set default login password
echo root:gig1234 | chpasswd

sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config
sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

rm -f /usr/bin/python
rm -f /usr/bin/python3
ln -s /usr/bin/python3.5 /usr/bin/python
ln -s /usr/bin/python3.5 /usr/bin/python3
