from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import render
from control import Status
from control.views import BaseView
from profile.models import SocketUser

BotUser = get_user_model()


class DeleteProfile(BaseView):
    template = "profile/delete_profile.html"

    @transaction.atomic()
    def post(self, request):
        data = Status(user=request.user, alert=True, success=False, message='Error updating profile!')

        if request.POST.get("delete", None) == "0":
            data.update({"message": "Deletion canceled!", "alert": True, "success": False})
            return render(request, "profile/profile_overview.html", data)

        elif request.POST.get("delete", None) == "1":
            if request.user.is_superuser:
                data.update({
                    "message": "Superusers can't delete themselves in the profile editor!",
                    "alert": True,
                    "success": False})
                return render(request, self.template, data)
            SocketUser.objects.get(user=request.user).delete()
            request.user.delete()
            data.update({'success': True, 'alert': True, 'message': 'User profile deleted!'})
            return render(request, "auth/login.html", data)
        return render(request, self.template, data)