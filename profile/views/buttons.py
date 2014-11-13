from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from control import Status
from control.socket_handler.client import SocketSender
from control.socket_handler.exceptions import SocketSenderError
from control.views import BaseView
from profile.models import SocketUser

BotUser = get_user_model()


class GetOps(BaseView):
    template = "profile/profile_overview.html"
    action = 'give_ops'
    restr = 'is_operator'

    def post(self, request):
        user = get_object_or_404(BotUser, username=request.user.username)
        data = Status(user=user, alert=True, success=False, message='Error regenerating token!')

        if not getattr(user, self.restr, None):
            data.update({'success': False,
                         'alert': True,
                         'message': 'You have no authorization to %s!' % self.action})
            return render(request, self.template, data)

        channel = request.POST.get('channel')
        if not channel or not channel.startswith('#') or channel == "#":
            data.update({'success': False, 'alert': True, 'message': "Faulty input"})
            return render(request, self.template, data)

        try:
            token = SocketUser.objects.get(user__username=user.username)
            command = settings.SOCKET_COMMANDS[self.action] % (user.nick, channel)
        except SocketUser.DoesNotExist:
            return render(request, self.template, data)

        try:
            send_2_socket(username=user.username, token=token, command=command)
        except SocketSenderError as e:
            data.update({'success': False, 'alert': True, 'message': e})
            return render(request, self.template, data)

        data.update({'success': True, 'alert': True, 'message': '%s send to bot!' % command})
        return render(request, self.template, data)


def send_2_socket(username, token, command):
    a = SocketSender(user=username, token=token, unix_socket=settings.LISTENER_SOCKET)
    a.connect()
    a.send(command)
    a.close()


class GetVoice(GetOps):
    restr = 'is_voice'
    action = 'give_voice'


class SendMessage(GetOps):
    action = 'send_msg'
    restr = 'registered'

    def post(self, request):
        user = get_object_or_404(BotUser, username=request.user.username)
        data = Status(user=user, alert=True, success=False, message='Error sending message to channel!')

        if not getattr(user, self.restr, None):
            data.update({'success': False,
                         'alert': True,
                         'message': 'You have no authorization to %s!' % self.action})
            return render(request, self.template, data)

        channel = request.POST.get('channel', None)
        message = request.POST.get('message', None)

        if not channel or not message:
            data.update({'success': False, 'alert': True, 'message': "Faulty input"})
            return render(request, self.template, data)

        try:
            token = SocketUser.objects.get(user__username=user.username)
            command = settings.SOCKET_COMMANDS[self.action] % (channel, message)
        except SocketUser.DoesNotExist:
            return render(request, self.template, data)

        try:
            send_2_socket(username=user.username, token=token, command=command)
        except SocketSenderError as e:
            data.update({'success': False, 'alert': True, 'message': e})
            return render(request, self.template, data)

        data.update({'success': True, 'alert': True, 'message': 'Message send by bot!'})
        return render(request, self.template, data)


class RegenerateToken(BaseView):
    template = "profile/profile_overview.html"
    action = 'regenerate_token'

    def post(self, request):
        user = get_object_or_404(BotUser, username=request.user.username)
        data = Status(user=user, alert=True, success=False, message='Invalid input for %s!' % self.action)

        try:
            action, value = request.POST.get(self.action).split('=')
        except AttributeError:
            return render(request, self.template, data)

        if action and action == self.action:
            if value == 'true':
                user.registration_token = None
                user.save()
                data.update({'success': True, 'alert': True, 'message': 'Registration token regenerated!'})
                return render(request, self.template, data)
        return render(request, self.template, data)