from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from profile.views.base_view import BaseView
from profile.views.buttons import GetVoice, GetOps, SendMessage
from profile.views.delete_profile import DeleteProfile
from profile.views.edit_profile import EditProfile
from profile.views.regenerate_token import RegenerateToken


urlpatterns = patterns(
    '',
    # Pages
    url(r'^/?$', login_required(BaseView.as_view()), name='profile_overview'),
    url(r'^edit/?$', login_required(EditProfile.as_view()), name='edit_profile'),
    url(r'^delete/?$', login_required(DeleteProfile.as_view()), name='delete_profile'),

    # Buttons
    url(r'^regenerate_token/?$', login_required(RegenerateToken.as_view()), name='regenerate_token'),
    url(r'^send_msg/?$', login_required(SendMessage.as_view()), name='send_msg'),
    url(r'^get_ops/?$', login_required(GetOps.as_view()), name='get_ops'),
    url(r'^get_voice/?$', login_required(GetVoice.as_view()), name='get_voice'),


)
