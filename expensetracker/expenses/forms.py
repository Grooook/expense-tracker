import datetime

from django import forms

from .models import Transaction
from .services import convert_str_to_datetime, get_time_now


class TransactionCreateForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(), required=False)
    date = forms.DateTimeField(required=False, initial=datetime.datetime.now().date, widget=forms.TextInput(
        attrs={'type': 'date'}
    ))
    time = forms.TimeField(required=False, initial=get_time_now(),  widget=forms.TextInput(
        attrs={'type': 'time'}
    ))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.user = self.request.user
        if 'data' in kwargs:
            self.date = kwargs['data']['date']
            self.time = kwargs['data']['time']
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        transaction = super().save(commit=False)
        transaction.user = self.user

        if self.data and self.time:
            transaction.date = convert_str_to_datetime(self.date, self.time)
        if commit:
            transaction.save()
        return transaction

    class Meta:
        model = Transaction
        fields = ('type', 'category', 'amount', 'currency',
                  'title', 'description', 'date', 'time')


class UpdateTransactionForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = Transaction
        fields = ('type', 'category', 'amount', 'currency',
                  'title', 'description')
