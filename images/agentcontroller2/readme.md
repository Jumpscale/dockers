
# agentcontroller2 image
Based on jumpscale/ubuntu:15.04 image. This images is an example on how to
build an configure jumpscale apps.
It simply uses `ays` to install agentcontroller2, agent2, and agentcontroller2 client

# How to test.
```
make test
```
The `test` target will build the image if it's not built already, and run
a simple test script that prints the `os info` as returned via the agent.
