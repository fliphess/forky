from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.views.generic import View
from control import Status


def logout_view(request):
    logout(request)
    return redirect('/')


class BaseView(View):
    template = None

    def get(self, request):
        return render(request, self.template, Status())


class IndexPage(View):
    def get(self, request):
        return render(request, 'base/main.html')