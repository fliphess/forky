from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from control import Status
from frontend.forms import EditProfileForm

BotUser = get_user_model()


class ProfileOverView(View):
    template = "frontend/profile_overview.html"

    def get(self, request, *args, **kwargs):
        data = Status()
        return render(request, self.template, data)


class EditProfile(View):
    template = "frontend/edit_profile.html"

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
            return render(request, "frontend/profile_overview.html", data)
        return render(request, self.template, data)


class DeleteProfile(View):
    template = "frontend/delete_profile.html"

    def get(self, request):
        return render(request, self.template, Status())

    @transaction.atomic()
    def post(self, request):
        user = get_object_or_404(BotUser, id=request.user.id)
        data = Status(user=user, alert=True, success=False, message='Error updating profile!')

        if request.POST.get("delete", None) == "0":
            data.update({"message": "Deletion canceled!", "alert": True, "success": False})
            return render(request, "frontend/profile_overview.html", data)

        elif request.POST.get("delete", None) == "1":
            if user.is_superuser:
                data.update({
                    "message": "Superusers can't delete themselves in the profile editor!",
                    "alert": True,
                    "success": False})
                return render(request, self.template, data)

            user.delete()
            data.update({'success': True, 'alert': True, 'message': 'User profile deleted!'})
            return render(request, "auth/login.html", data)
        return render(request, self.template, data)


class RegenerateToken(View):
    template = "frontend/profile_overview.html"

    def get(self, request):
        return render(request, self.template, Status())

    def post(self, request):
        user = get_object_or_404(BotUser, username=request.user.username)
        data = Status(user=user, alert=True, success=False, message='Error regenerating token!')

        if request.POST.get("regenerate_token", None) == "1":
            user.registration_token = None
            user.save()
            data.update({'success': True, 'alert': True, 'message': 'Registration token regenerated!'})
        return render(request, self.template, data)
