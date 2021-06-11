from django import forms
from .models import AdvUser, Task
from .apps import user_joined
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Неверное имя пользователя или пароль"
        ),
        'inactive': _("This account is inactive."),
    }
    password = forms.CharField(
        label=_("Password"),
        min_length=8,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )


class JoinForm(forms.ModelForm):
    email = forms.CharField(
        required=True, label='Адрес электронной почты'
    )
    username = forms.CharField(
        required=True, min_length=6, label='Имя пользователя'
    )
    password1 = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label='Повторите пароль', widget=forms.PasswordInput(),
    )

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get('password1', None)
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
              'Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_joined.send(JoinForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2')


class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'image', 'biography')


class CreateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('title', 'content')
