

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Server
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

import sys, os, django
sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "control.settings")
from django import setup as django_setup
from django.conf import settings
django_setup()

from modules.fix.socket_listener import SocketHandler
p = SocketHandler(pidfile='/tmp/pidfile', unix_socket='/tmp/irc.sock')
p.bind()

for i in p.receive():
  print i

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Sender
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


from send_2_socket import SocketSender
a = SocketSender(user='flip', token='mc3nT8TEzlZvWuk0UP5zYr47MtrdxhfkE2V2hJVbqUPT8Pp5M0h9IzTZ86Xm', unix_socket='/tmp/irc.sock')
a.connect()
a.send('plop')






