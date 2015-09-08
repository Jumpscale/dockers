NAME = jumpscale/agentcontroller2
VERSION = 15.04
CONTEXT = ./
BASEIMAGE = ../../baseimage/image

.PHONY: all build prepare clean

all: build

build: check
	docker build -t $(NAME):$(VERSION) --rm $(CONTEXT)

check:
	docker images | grep jumpscale/ubuntu | grep $(VERSION) || ( echo 'ERROR: Please build jumpscale/ubuntu:$(VERSION) first!' && exit 1 )

