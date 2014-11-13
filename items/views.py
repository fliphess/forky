from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from control import Status
from control.socket_handler.exceptions import SocketSenderError
from items.forms import AddQuoteForm
from items.models import Quote, InfoItem
from profile.models import SocketUser
from profile.views.buttons import send_2_socket

BotUser = get_user_model()


class QuotesView(View):
    data = Status()
    template = "items/quotes.html"
    model = Quote

    def get(self, request):
        quotes = [i for i in enumerate(Quote.objects.filter(user__username=request.user.username))]
        self.data.add({"quotes": quotes})
        return render(request, self.template, self.data)


class ShowQuote(View):
    data = Status()
    template = "items/quote.html"
    model = Quote

    def get(self, request, pk):
        quote = get_object_or_404(self.model, pk=pk)
        self.data.add({"quote": quote})
        return render(request, self.template, self.data)


class AddQuote(View):
    template = "items/add_quote.html"
    data = Status(message="Fill in all fields to add a quote", success=True, alert=True)

    def get(self, request):
        self.data.add({"form": AddQuoteForm})
        return render(request, self.template, self.data)

    @transaction.atomic()
    def post(self, request):
        form = AddQuoteForm(request.POST)
        if form.is_valid():
            quote = form.clean()["quote"]
            Quote.objects.create(user=request.user, quote=quote)
            self.data.add({"message": "Quote added", "success": True, "quotes": Quote.objects.all()})
            return render(request, self.template, self.data)
        else:
            self.data.update({"message": 'Invalid input', "success": False, "alert": True})
            return self.get(request=request)


class DeleteQuote(View):
    template = "items/delete_quote.html"
    data = Status(alert=True, success=False, message='Error deleting quote!')

    def get(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        self.data.update({'quote': quote})
        return render(request, self.template, self.data)

    @transaction.atomic()
    def post(self, request, pk):
        self.data.update({'quotes': Quote.objects.all()})

        quote = get_object_or_404(Quote, pk=pk)

        if not quote.user.username == request.user.username:
            self.data.update({"message": "A user can only delete it's own quotes!", "alert": True, "success": False})
            return render(request, self.template, self.data)

        if request.POST.get("delete", None) == "0":
            self.data.update({"message": "Deletion canceled!", "alert": True, "success": False})
            return render(request, self.template, self.data)

        elif request.POST.get("delete", None) == "1":
            quote.delete()
            self.data.update({'success': True, 'alert': True, 'message': 'Quote deleted!'})
        return render(request, "items/quotes.html", self.data)


class InfoItemView(View):
    data = Status()
    template = "items/infoitems.html"
    action = 'send_item'
    restr = 'registered'

    def get(self, request):
        items = InfoItem.objects.all()
        self.data.add({"items": items})
        return render(request, self.template, self.data)


class SendInfoItemToChannel(InfoItemView):
    def post(self, request, pk):
        item = get_object_or_404(InfoItem, pk=pk)
        user = get_object_or_404(BotUser, username=request.user.username)

        items = InfoItem.objects.all()
        data = Status(user=user, alert=True, success=False, message='Error sending to channel!', items=items)

        if not getattr(user, self.restr, None):
            data.update({
                'success': False,
                'alert': True,
                'message': 'You have no authorization to %s!' % self.action})
            return render(request, self.template, data)

        channel = request.POST.get('channel', None)
        if not channel:
            data.update({'success': False, 'alert': True, 'message': "Faulty input"})
            return render(request, self.template, data)

        try:
            token = SocketUser.objects.get(user__username=user.username)
            command = settings.SOCKET_COMMANDS[self.action] % (channel, item.item, item.text)
        except (SocketUser.DoesNotExist, KeyError, TypeError):
            return render(request, self.template, data)

        try:
            send_2_socket(username=user.username, token=token, command=command)
        except SocketSenderError as e:
            data.update({'success': False, 'alert': True, 'message': 'Error: %s' % e})
            return render(request, self.template, data)

        data.update({'success': True, 'alert': True, 'message': 'Message send by bot!'})
        return render(request, self.template, data)
