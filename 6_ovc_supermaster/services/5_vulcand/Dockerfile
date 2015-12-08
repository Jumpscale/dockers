FROM scratch

MAINTAINER GreenITGlobe

COPY vulcand /app/vulcand
COPY vctl /app/vctl
COPY vbundle /app/vbundle

ENV PATH=/app:$PATH

ENTRYPOINT ["/app/vulcand"]
CMD ["-etcd=http://127.0.0.1:4001", "-etcd=127.0.0.1:4002", "-etcd=127.0.0.1:4003", "-sealKey=1b727a055500edd9ab826840ce9428dc8bace1c04addc67bbac6b096e25ede4b"]
