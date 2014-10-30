from django.forms import ModelForm
from items.models import Quote


class AddQuoteForm(ModelForm):
    class Meta:
        model = Quote
        exclude = ('user', 'date_added',)
