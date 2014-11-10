from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from control import Status
from items.forms import AddQuoteForm
from items.models import Quote


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

        return render(request, self.template, self.data)
