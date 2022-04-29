from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm
)
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from accounts.forms import CustomUserCreationForm, UserProfileForm


class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.id])


class UserLogoutView(LogoutView):
    template_name = 'logout.html'


class UserSignupView(CreateView):
    # form_class = UserCreationForm
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


# class UserProfileView(DetailView):
#     model = User
#     # template_name = 'profile.html'
#     template_name = 'lk.html'
#     context_object_name = 'profile'


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'lk.html'
    # context_object_name = 'profile_form'
