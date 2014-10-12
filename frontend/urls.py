# from django.conf.urls import patterns, include, url
# from django.contrib import admin
# from django.contrib.auth.decorators import login_required
# from frontend.views import CommandOverView, CommandEditor, AddCommand, EditCommand, DeleteCommand, CommandExecutor
#
# admin.autodiscover()
#
# urlpatterns = patterns(
#     '',
#     url(r'^/?$', login_required(CommandOverView.as_view()), name='command_overview'),
#     url(r'^command_editor/?$', login_required(CommandEditor.as_view()), name='command_editor'),
#     url(r'^executor/(?P<name>\w+)/?$', CommandExecutor.as_view(), name='command_executor'),
#
#
#     url(r'^add_command/$', login_required(AddCommand.as_view()), name='add_command'),
#     url(r'^edit_command/(?P<name>\w+)/$', login_required(EditCommand.as_view()), name='edit_command'),
#     url(r'^delete_command/(?P<name>\w+)/$', login_required(DeleteCommand.as_view()), name='delete_command'),
# )
