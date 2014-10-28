from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from control import Status
from profile.forms import EditProfileForm
BotUser = get_user_model()


class EditProfile(View):
    template = "profile/edit_profile.html"

    def get(self, request):
        user = get_object_or_404(BotUser, username=request.user.username)
        initial = {
            "first_name": user.first_name or 'To be set',
            "last_name": user.last_name or 'To be set',
            "email": user.email,
            "nick": user.nick,
            "host": user.host,
            "about": user.about,
        }
        return render(request, self.template, Status(form=EditProfileForm(initial=initial)))

    @transaction.atomic()
    def post(self, request):
        form = EditProfileForm(request.POST)
        user = get_object_or_404(BotUser, id=request.user.id)
        data = Status(form=form, alert=True, success=False, message='Error updating profile!')
        if form.is_valid():
            user.first_name = form.clean()['first_name']
            user.last_name = form.clean()['last_name']
            user.email = form.clean()['email']
            user.nick = form.clean()['nick']
            user.host = form.clean()['host']
            user.about = form.clean()['about']
            user.save(force_update=True)

            data.update({'form': form, 'success': True, 'alert': True, 'message': 'User profile updated!'})
            return render(request, "profile/profile_overview.html", data)
        return render(request, self.template, data)