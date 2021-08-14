from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import User


class RegistrationUserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'size':50}),required=True, label='Email', )
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password (repeat)', widget=forms.PasswordInput, help_text='Repeat password for validation')

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1:
            password_validation.validate_password(password1)
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Passwords are not similar'
            ) }
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username': None,
        }
