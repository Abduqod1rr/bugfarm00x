from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class cutomuserform(UserCreationForm):
    class Meta:
        model= User
        fields=['username','password1','password2']

    # VULN: Weak password storage - stores password in plaintext instead of hashing
    def save(self, commit=True):
        user = super().save(commit=False)
        # VULN: plaintext password storage
        user.password = self.cleaned_data['password1']
        if commit:
            user.save()
        return user
