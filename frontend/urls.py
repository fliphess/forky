from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from frontend.views import ProfileOverView, EditProfile, DeleteProfile, RegenerateToken


urlpatterns = patterns(
    '',
    url(r'^/?$', login_required(ProfileOverView.as_view()), name='profile_overview'),
    url(r'^edit/?$', login_required(EditProfile.as_view()), name='edit_profile'),
    url(r'^delete/?$', login_required(DeleteProfile.as_view()), name='delete_profile'),
    url(r'^regenerate_token/?$', login_required(RegenerateToken.as_view()), name='regenerate_token'),
)
