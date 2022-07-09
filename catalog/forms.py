from django.forms import *
import datetime
from .models import BookInstance


class RenewBookForm(Form):
    renewal_date = DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data.get('renewal_date')

        if data < datetime.date.today():
            raise ValidationError('Invalid date - renewal in past')

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError('Invalid date - renewal more than 4 weeks ahead')

        return data


class RenewBookModelForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {
            'due_back': 'New renewal date'
        }
        help_texts = {
            'due_back': "Enter a date between now and 4 weeks (default 3)"
        }

    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise ValidationError('Invalid date - renewal in past')

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError('Invalid date - renewal date more than 4 weeks ahead')

        return data
