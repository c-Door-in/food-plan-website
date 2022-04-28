from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, PasswordChangeForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name',)
        field_classes = {"username": UsernameField}


class UserProfileForm(forms.ModelForm):
    # password2 = forms.CharField(
    #     label="Password confirmation",
    #     widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    #     strip=False,
    #     help_text="Enter the same password as before, for verification.",
    # )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['email'].required = True
        self.fields['username'].label = 'Логин'

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name',)
        field_classes = {"username": UsernameField}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'PasswordConfirm'}),
        }


# class UserProfileForm(UserCreationForm):
#     password1 = forms.CharField(
#         label="Password",
#         strip=False,
#         widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control', 'id': 'password'}),
#     )
#     password2 = forms.CharField(
#         label="Password confirmation",
#         widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control', 'id': 'PasswordConfirm'}),
#         strip=False,
#         help_text="Enter the same password as before, for verification."
#     )
#
#     class Meta:
#         model = User
#         fields = UserCreationForm.Meta.fields + ('first_name', 'password2')
#         field_classes = {"username": UsernameField}
#         widgets = {
#             'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
#             'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'email'}),
#             'password2': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'PasswordConfirm'}),
#         }
