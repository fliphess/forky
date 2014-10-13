from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic.base import TemplateView

from registration.backend.views import ActivationView
from registration.backend.views import RegistrationView


urlpatterns = patterns(
    '',
    url(r'^activate/complete/$',
        TemplateView.as_view(template_name='registration/activation_complete.html'),
        name='registration_activation_complete'),

    url(r'^activate/(?P<activation_key>\w+)/$',
        ActivationView.as_view(),
        name='registration_activate'),

    url(r'^register/$',
        RegistrationView.as_view(),
        name='registration_register'),

    url(r'^register/complete/$',
        TemplateView.as_view(template_name='registration/registration_complete.html'),
        name='registration_complete'),

    url(r'^register/closed/$',
        TemplateView.as_view(template_name='registration/registration_closed.html'),
        name='registration_disallowed'),

    url(r'', include('registration.urls')),
)
