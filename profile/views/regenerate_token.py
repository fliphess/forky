from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from control import Status
from profile.views.base_view import BaseView
BotUser = get_user_model()


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