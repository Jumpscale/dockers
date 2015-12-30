#!/bin/bash
set -e
source /bd_build/buildconfig
set -x


$minimal_apt_get_install curl less mc iproute2 iputils-arping inetutils-telnet inetutils-ftp rsync inetutils-traceroute iputils-ping iputils-tracepath iputils-clockdiff

$minimal_apt_get_install net-tools sudo python

$minimal_apt_get_install git wget tmux

#rm -rf /usr/bin/python
#ln /usr/bin/python3.5 /usr/bin/python

## This tool runs a command as another user and sets $HOME.
cp /bd_build/bin/setuser /sbin/setuser

#Enable SSHD
rm /etc/service/sshd/down

#Pregenerate the host SSH keys
dpkg-reconfigure openssh-server

#Set default login password
echo root:gig1234 | chpasswd

sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
