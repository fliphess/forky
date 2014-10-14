from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model

BotUser = get_user_model()


class EditProfileForm(forms.Form):
    first_name = forms.CharField(required=True, label="First name")
    last_name = forms.CharField(required=True, label="Last name")
    email = forms.EmailField(required=True, label="Email address")
    nick = forms.RegexField(
        regex=r'^[a-z_\-\[\]\\^{}|`]{0,15}$',
        max_length=15,
        label="Nickname",
        error_messages={'invalid': "Invalid nickname!"})
    host = forms.CharField(required=True, label="Host mask")
    about = forms.CharField(widget=forms.Textarea)

    def clean_nickname(self):
        if BotUser.objects.filter(nick=self.cleaned_data['nick']):
            raise forms.ValidationError('This nickname is already claimed by another user.')

    def clean_email(self):
        if BotUser.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError("This email address is already in use. "
                                        "Please supply a different email address.")

        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in settings.EMAIL_BAD_DOMAIN_LIST:
            raise forms.ValidationError("This email provider is listed as prohibited!"
                                        "Please supply a different email address.")
        return self.cleaned_data['email']

    def clean(self):
        return self.cleaned_data