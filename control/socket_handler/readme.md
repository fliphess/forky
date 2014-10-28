# IRC bot socket handler 

Runs a little server listening on a local unix socket. 
Provides auth and encryption

## Run Server
```python

    import sys, os, django
    sys.path.append(".")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "control.settings")

    from django import setup as django_setup
    from django.conf import settings
    django_setup()
 
    from control.socket_handler.server import SocketServer
    p = SocketServer(unix_socket=settings.LISTENER_SOCKET)
    p.bind()

    for i in p.receive():
        print i
```

# Send to server
```python
 
    from control.socket_handler.client import SocketSender
    a = SocketSender(user='flip', token='mc3nT8TEzlZvWuk0UP5zYr47MtrdxhfkE2V2hJVbqUPT8Pp5M0h9IzTZ86Xm', unix_socket='/tmp/ircbot.sock')
    a.connect()
    a.send('plop')
    a.close()
```






