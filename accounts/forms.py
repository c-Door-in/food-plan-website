from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UsernameField, PasswordChangeForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'autofocus': True,
        'class': 'form-control',
        'id': 'email',
        'aria-describedby': 'emailHelp'
    }))
    password = forms.CharField(label='Логин', strip=False, widget=forms.PasswordInput(attrs={
        'autocomplete': 'current-password',
        'class': 'form-control',
        'id': 'password'
    }),
    )


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs.pop("autofocus", None)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name',)


class ProfileForm(forms.ModelForm):
    error_messages = {
        'password_mismatch": "The two password fields didn’t match.',
    }
    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='New password confirmation',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='Enter the same password as before, for verification.',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['username'].required = True
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['first_name', 'username']

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        password_validation.validate_password(password2, self.instance)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        user = super().save(commit=False)
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


