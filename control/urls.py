from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from control.views import IndexPage

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', login_required(IndexPage.as_view()), name='main'),
    url(r'^start/$', login_required(IndexPage.as_view()), name='start'),

    url(r'^profile/', include('profile.urls')),
    url(r'^items/', include('items.urls')),
    url(r'^chat/', include('chat.urls')),

    url(r'^accounts/', include('registration.backend.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$', 'control.views.logout_view', name='logout'),
)
