from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from items.views import AddQuote, QuotesView, DeleteQuote, ShowQuote


urlpatterns = patterns(
    '',
    # Quotes
    url(r'^quotes/?$', login_required(QuotesView.as_view()), name='quotes'),
    url(r'^quotes/show/(?P<pk>\d+)?$', login_required(ShowQuote.as_view()), name='show'),

    url(r'^quotes/add/?$', login_required(AddQuote.as_view()), name='add_quote'),
    url(r'^quotes/delete/(?P<pk>\d+)?$', login_required(DeleteQuote.as_view()), name='delete_quote'),

    # Info items
    # TODO
)
