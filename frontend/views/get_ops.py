from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from control import Status
from control.socket_handler.client import SocketSender
from control.socket_handler.exceptions import SocketSenderError
from frontend.models import SocketUser
from frontend.views.base_view import BaseView

BotUser = get_user_model()


class GetOps(BaseView):
    action = 'get_ops'

    def post(self, request):
        user = get_object_or_404(BotUser, username=request.user.username)
        data = Status(user=user, alert=True, success=False, message='Error regenerating token!')

        if not request.POST.get("get_ops", None) == "1":
            return render(request, self.template, data)

        if not user.is_operator():
            data.update({'success': False, 'alert': True, 'message': 'You have no authorization for ops!'})
            return self.get(request)

        action, channel = request.POST.get(self.action).split('=')
        if not action or not channel or not 
        try:
            token = SocketUser.objects.get(user__username=user.username)
            command = settings.SOCKET_COMMANDS[self.action] % ()
        except SocketUser.DoesNotExist:
            return render(request, self.template, data)

        try:
            send_2_socket(username=user.username, token=token, command=command)

        except SocketSenderError as e:
            data.update({'success': False, 'alert': True, 'message': '!'})
            return render(request, self.template, data)

        data.update({'success': True, 'alert': True, 'message': 'Registration token regenerated!'})
        return render(request, self.template, data)



def send_2_socket(username, token, command):
    a = SocketSender(user=username, token=token, unix_socket=settings.LISTENER_SOCKET)
    a.connect()
    a.send(command)
    a.close()