Full documentation [here](https://gig.gitbooks.io/jumpscale-core8/content/GettingStarted/JSDockers.html)


# How To Use


## preparation

- on your machine clone this repo

```python
j.tools.develop.init(["ovh4"])
j.tools.develop.syncCode(monitor=True)

Make a selection please:
   1: /Users/despiegk/opt/code/github/jumpscale/1
   2: /Users/despiegk/opt/code/github/jumpscale/Tcp-DNS-proxy
   3: /Users/despiegk/opt/code/github/jumpscale/alpine-sshd
   4: /Users/despiegk/opt/code/github/jumpscale/ays_jumpscale8
   5: /Users/despiegk/opt/code/github/jumpscale/dev_process
   6: /Users/despiegk/opt/code/github/jumpscale/dnslib
   7: /Users/despiegk/opt/code/github/jumpscale/dockers
   8: /Users/despiegk/opt/code/github/jumpscale/geventSocks5
   9: /Users/despiegk/opt/code/github/jumpscale/go-raml
   10: /Users/despiegk/opt/code/github/jumpscale/jscockpit
   11: /Users/despiegk/opt/code/github/jumpscale/jumpscale_ays8_testenv
   12: /Users/despiegk/opt/code/github/jumpscale/jumpscale_core8
   13: /Users/despiegk/opt/code/github/jumpscale/jumpscale_portal8
   14: /Users/despiegk/opt/code/github/jumpscale/ledisdb
   15: /Users/despiegk/opt/code/github/jumpscale/lua
   16: /Users/despiegk/opt/code/github/jumpscale/mitmproxy
   17: /Users/despiegk/opt/code/github/jumpscale/offline
   18: /Users/despiegk/opt/code/github/jumpscale/play8
   19: /Users/despiegk/opt/code/github/jumpscale/playenv
   20: /Users/despiegk/opt/code/github/jumpscale/pymiproxy
   21: /Users/despiegk/opt/code/github/jumpscale/smart_office
   22: /Users/despiegk/opt/code/github/jumpscale/smartproxy
   23: /Users/despiegk/opt/code/github/jumpscale/tamper

Select Nr, use comma separation if more e.g. "1,4", * is all, 0 is None: 7,12

```

- now ssh into your build machine (in this example ovh4)


## for individual builds


```bash
cd /opt/code/github/jumpscale/dockers/js8/x86_64
python3 buildall.py
```

## master builder

on build machine, code will be kept in sync from the developer tools

```bash
cd /opt/code/github/jumpscale/dockers/js8/x86_64/51_ubuntu1604_js8_master_buildscript
python3 build.py
```
