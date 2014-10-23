from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404, render
from control import Status
from frontend.views.base_view import BaseView

BotUser = get_user_model()

class DeleteProfile(BaseView):
    template = "frontend/delete_profile.html"

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