#Dockerfile for https://github.com/Gaff/alpine-sshd
FROM duportal/rpi-alpine:latest

#Build script installs sshd
COPY build.sh /build.sh
RUN chmod 755 /build.sh
RUN /build.sh
RUN rm build.sh

#Die a bit faster on exit:
ENV S6_KILL_GRACETIME=500

RUN apk add --update --virtual=build-dependencies wget ca-certificates && \
    export ALPINE_GLIBC_BASE_URL="https://circle-artifacts.com/gh/andyshinn/alpine-pkg-glibc/6/artifacts/0/home/ubuntu/alpine-pkg-glibc/packages/x86_64" && \
    export ALPINE_GLIBC_PACKAGE="glibc-2.21-r2.apk" && \
    export ALPINE_GLIBC_BIN_PACKAGE="glibc-bin-2.21-r2.apk" && \
    wget "$ALPINE_GLIBC_BASE_URL/$ALPINE_GLIBC_PACKAGE" "$ALPINE_GLIBC_BASE_URL/$ALPINE_GLIBC_BIN_PACKAGE" && \
    apk add --allow-untrusted "$ALPINE_GLIBC_PACKAGE" "$ALPINE_GLIBC_BIN_PACKAGE" && \
    /usr/glibc/usr/bin/ldconfig "/lib" "/usr/glibc/usr/lib" && \
    echo 'hosts: files mdns4_minimal [NOTFOUND=return] dns mdns4' >> /etc/nsswitch.conf && \
    apk del build-dependencies && \
    rm "$ALPINE_GLIBC_PACKAGE" "$ALPINE_GLIBC_BIN_PACKAGE" /var/cache/apk/*

#Script to generate host keys on startup:
COPY keygen.sh /etc/cont-init.d/keygen
RUN chmod 755 /etc/cont-init.d/keygen

EXPOSE 22

#-D = don't detach, -e = output to stderr, -f = config file
CMD [ "/usr/sbin/sshd", "-D", "-e", "-f", "/etc/ssh/sshd_config"]

COPY build/opt /opt

