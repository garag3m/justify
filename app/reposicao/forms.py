
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms.fields import HiddenInput
from .models import UUIDUser

# User: create
class UUIDUserForm(forms.ModelForm):

    is_company = forms.BooleanField(widget=forms.HiddenInput(), initial=True)

    def save(self, commit=True):
        user = super(UUIDUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = UUIDUser
        fields = ('username', 'first_name','last_name','cpf', 'email','password')
        labels = {
            'username': 'Usuário',
            'first_name': 'Primeiro nome',
            'last_name': 'Último nome',
            'cpf': 'CPF',
            'email': 'Email',
        }
        widgets={
            'password':forms.PasswordInput()
        }
