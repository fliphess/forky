"""
URL patterns for the views included in ``django.contrib.auth``.

Including these URLs (via the ``include()`` directive) will set up the
following patterns based at whatever URL prefix they are included
under:

* User login at ``login/``.

* User logout at ``logout/``.

* The two-step password change at ``password/change/`` and
  ``password/change/done/``.

* The four-step password reset at ``password/reset/``,
  ``password/reset/confirm/``, ``password/reset/complete/`` and
  ``password/reset/done/``.

The default registration backend already has an ``include()`` for
these URLs, so under the default setup it is not necessary to manually
include these views. Other backends may or may not include them;
consult a specific backend's documentation for details.

"""

from django.conf.urls import patterns, include
from django.conf.urls import url
from django.contrib.auth.views import password_change, password_change_done, password_reset, password_reset_confirm, \
    password_reset_complete, password_reset_done


urlpatterns = patterns(
    '',
    (r'', include('django.contrib.auth.urls')),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}, name='auth_login'),
    url(r'^logout/$', 'control.views.auth.logout_view', name='auth_logout'),

    url(r'^password/change/$',
        password_change,
        name='auth_password_change'),

    url(r'^password/change/done/$',
        password_change_done,
        name='auth_password_change_done'),

    url(r'^password/reset/$',
        password_reset,
        name='auth_password_reset'),

    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        name='auth_password_reset_confirm'),

    url(r'^password/reset/complete/$',
        password_reset_complete,
        name='auth_password_reset_complete'),

    url(r'^password/reset/done/$',
        password_reset_done,
        name='auth_password_reset_done'),
)
