from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.views.generic.edit import CreateView, UpdateView


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm


class UserLogoutView(LogoutView):
    template_name = 'logout.html'
