from django.shortcuts import render
from django.views.generic import View
from control import Status


class BaseView(View):
    template = "frontend/profile_overview.html"

    def get(self, request):
        return render(request, self.template, Status())