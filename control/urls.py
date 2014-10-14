from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from control.views.base import IndexPage

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', login_required(IndexPage.as_view()), name='main'),
    url(r'^start/$', login_required(IndexPage.as_view()), name='start'),

    url(r'^profile/', include('frontend.urls')),
    url(r'^accounts/', include('registration.backend.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$', 'control.views.auth.logout_view', name='logout'),
)
