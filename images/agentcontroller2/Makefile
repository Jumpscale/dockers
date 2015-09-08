NAME = jumpscale/agentcontroller2
VERSION = 15.04
CONTEXT = ./
BASEIMAGE = ../../baseimage/image

TEST_CONTAINER = ag2test

.PHONY: all build prepare clean

all: build

build: check-build
	docker build -t $(NAME):$(VERSION) --rm $(CONTEXT)

check-build:
	docker images | grep jumpscale/ubuntu | grep $(VERSION) || ( echo 'ERROR: Please build jumpscale/ubuntu:$(VERSION) first!' && exit 1 )

test: build
	docker stop $(TEST_CONTAINER) || true
	docker rm $(TEST_CONTAINER) || true
	docker run -d --name $(TEST_CONTAINER) $(NAME):$(VERSION)
	# wait until the image is fully booted
	echo 'Wait for 10 seconds until the image is fully booted (hopefully)'
	sleep 10s
	docker exec -ti $(TEST_CONTAINER) jspython -c "from JumpScale import j; print j.clients.ac.getByInstance('main').get_os_info(1, 1)"
