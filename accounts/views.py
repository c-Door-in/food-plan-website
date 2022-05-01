from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from accounts.forms import CustomUserCreationForm, ProfileForm, CustomAuthenticationForm
from website.models import Subscribe


class CustomLoginView(LoginView):
    template_name = 'auth.html'
    form_class = CustomAuthenticationForm

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.id])


class CustomLogoutView(LogoutView):
    next_page = 'login'


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'lk.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscribes'] = Subscribe.objects.filter(subscriber=self.request.user.id)
        return context

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.id])
