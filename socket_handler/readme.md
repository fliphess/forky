

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

import sys, os, django
sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "control.settings")
from django import setup as django_setup
from django.conf import settings
django_setup()

from modules.fix.socket_listener import SocketHandler
p = SocketHandler(pidfile='/tmp/pidfile', unix_socket='/tmp/irc.sock')
p.connect()

p.send('lredkhmdxflt')






