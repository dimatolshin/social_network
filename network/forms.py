from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import Profile

User = get_user_model()


class CreateNewUser(UserCreationForm):
    birth_date = forms.DateField(initial=timezone.now().date(), widget=forms.SelectDateWidget)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "birth_date", "password1", "password2",)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.birth_date = self.cleaned_data['birth_date']
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user

