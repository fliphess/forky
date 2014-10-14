from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from frontend.forms import EditProfileForm

BotUser = get_user_model()


class ProfileOverView(View):
    template = "frontend/profile_overview.html"

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(BotUser, username=request.user.username)
        self.data = {
            "user": user,
            "message": "something to tell you whatever that might be",
            "alert": True,
        }
        return render(request, self.template, self.data)


class EditProfile(View):
    template = "frontend/edit_profile.html"

    def get(self, request):
        user = get_object_or_404(BotUser, id=request.user.id)
        initial = {
            "first_name": user.first_name or 'To be set',
            "last_name": user.last_name or 'To be set',
            "email": user.email,
            "nick": user.nick,
            "host": user.host,
            "about": user.about,
        }
        form = EditProfileForm(initial=initial)
        data = { "form": form, "user": user, "success": True, "alert": "success", "message": "Something"}
        return render(request, self.template, data)


    @transaction.atomic()
    def post(self, request):
        form = EditProfileForm(request.POST)
        user = get_object_or_404(BotUser, id=request.user.id)

        if form.is_valid():
            user.first_name = form.clean()['first_name']
            user.last_name = form.clean()['last_name']
            user.email = form.clean()['email']
            user.nick = form.clean()['nick']
            user.host = form.clean()['host']
            user.about = form.clean()['about']
            user.save(force_update=True)
            return render(request, "frontend/profile_overview.html", {"user": user})
        return render(request, self.template, {"user": user})


class DeleteProfile(View):
    template = "frontend/delete_profile.html"

    def get(self, request):
        user = get_object_or_404(BotUser, id=request.user.id)
        return render(request, self.template, {"user": user})

    @transaction.atomic()
    def post(self, request):
        user = get_object_or_404(BotUser, id=request.user.id)
        if request.POST.get("delete", None) == "1":
            user.delete()
            return render(request, "auth/login.html")
        return render(request, self.template, {"user": user})
