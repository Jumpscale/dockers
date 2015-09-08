NAME = jumpscale/ubuntu
VERSION = 15.10
CONTEXT = /tmp/$(NAME)-$(VERSION)
BASEIMAGE = ../../baseimage/image

.PHONY: all build prepare clean

all: build

build: clean prepare
	docker build -t $(NAME):$(VERSION) --rm $(CONTEXT)

prepare:
	mkdir -p $(CONTEXT)
	cp -r $(BASEIMAGE)/* $(CONTEXT)/
	cp -r ../../runit $(CONTEXT)/
	cp ./Dockerfile $(CONTEXT)/

clean:
	rm -rf $(CONTEXT)
