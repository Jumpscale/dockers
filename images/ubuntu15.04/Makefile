NAME = jumpscale/ubuntu
VERSION = 15.04
CONTEXT = /tmp/$(NAME)-$(VERSION)

all: build

build: prepare
	docker build -t $(NAME):$(VERSION) --rm $(CONTEXT)

prepare:
	mkdir -p $(CONTEXT)
	cp -r ../baseimage/image/* $(CONTEXT)/
	cp ./Dockerfile $(CONTEXT)/
