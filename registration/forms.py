"""
Forms and validation code for user registration.

Note that all of these forms assume Django bundle default ``User``
model; since it's not possible for a form to anticipate in advance the
needs of custom user models, you will need to write your own forms if
you're using a custom model.

"""


from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()

class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """
    required_css_class = 'required'
    
    username = forms.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=30,
        label=_("Username"),
        error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})

    email = forms.EmailField(label=_("E-mail"))

    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label=_("Password"))

    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label=_("Password (again)"))

    tos = forms.BooleanField(
        widget=forms.CheckboxInput,
        label=_(u'I will not be an asshole'),
        error_messages={'required': _("I will not be an asshole")})

    def clean_username(self):
        """ Validate that the username is alphanumeric and is not already in use.
        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        """ Validate that the supplied email address is unique for the site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. "
                                          "Please supply a different email address."))

        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in settings.EMAIL_BAD_DOMAIN_LIST:
            raise forms.ValidationError(_("This email provider is listed as prohibited!"
                                          "Please supply a different email address."))
        return self.cleaned_data['email']

    def clean(self):
        """
        Verify that the values entered into the two password fields match.
        Note that an error here will end up in ``non_field_errors()`` because it doesn't apply to a single field.
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data
