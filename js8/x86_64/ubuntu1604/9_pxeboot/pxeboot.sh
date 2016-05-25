#!/usr/bin/env bash
set -e
source /code/buildconfig
set -x


$minimal_apt_get_install dnsmasq dnsmasq-utils
$minimal_apt_get_install pxelinux syslinux syslinux-common


export TARGET_DIR=/build/pxeboot

mkdir -p $TARGET_DIR

# dnsmasq
cp /usr/sbin/dnsmasq $TARGET_DIR
cp -R /code/services/6_pxeboot/conf $TARGET_DIR

# tftpboot
cp -R /code/services/6_pxeboot/tftpboot $TARGET_DIR

cp /usr/lib/syslinux/modules/bios/ldlinux* $TARGET_DIR/tftpboot
cp /usr/lib/PXELINUX/pxelinux.0 $TARGET_DIR/tftpboot
