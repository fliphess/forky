from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from items.views import AddQuote, QuotesView, DeleteQuote


urlpatterns = patterns(
    '',
    url(r'^/?$', login_required(QuotesView.as_view()), name='quotes'),
    url(r'^add/?$', login_required(AddQuote.as_view()), name='add_quote'),
    url(r'^delete/?$', login_required(DeleteQuote.as_view()), name='delete_quote'),
)
