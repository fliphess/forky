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
    def post(self, request):
        user = get_object_or_404(BotUser, username=request.user.username)
        data = Status(user=user, alert=True, success=False, message='Error regenerating token!')

        if not user.is_operator:
            data.update({'success': False,
                         'alert': True,
                         'message': 'You have no authorization to run %s!' % self.action})
            return render(request, self.template, data)

        channel = request.POST.get('channel')
        if not channel or not channel.startswith('#'):
            data.update({'success': False, 'alert': True, 'message': "Faulty input"})
            return render(request, self.template, data)

        try:
            token = SocketUser.objects.get(user__username=user.username)
            command = settings.SOCKET_COMMANDS['give_ops'] % (user.nick, channel)
        except SocketUser.DoesNotExist:
            return render(request, self.template, data)

        try:
            self.send_2_socket(username=user.username, token=token, command=command)
        except SocketSenderError as e:
            data.update({'success': False, 'alert': True, 'message': e})
            return render(request, self.template, data)

        data.update({'success': True, 'alert': True, 'message': 'Registration token regenerated!'})
        return render(request, self.template, data)

    @staticmethod
    def send_2_socket(username, token, command):
        a = SocketSender(user=username, token=token, unix_socket=settings.LISTENER_SOCKET)
        a.connect()
        a.send(command)
        a.close()