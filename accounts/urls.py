from django.urls import path

from accounts import views

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    # path('update/<int:pk>/', views.UserUpdateView.as_view(), name='update'),
    # path("password_change/", views.UserPasswordChangeView.as_view(), name="password_change"),
    # path("password_change/done/", views.UserPasswordChangeDoneView.as_view(), name="password_change_done",),
    # path("password_reset/", views.UserPasswordResetView.as_view(), name="password_reset"),
    # path("password_reset/done/", views.UserPasswordResetDoneView.as_view(), name="password_reset_done",),
    # path("reset/<uidb64>/<token>/", views.UserPasswordResetConfirmView.as_view(), name="password_reset_confirm",),
    # path("reset/done/", views.UserPasswordResetCompleteView.as_view(), name="password_reset_complete",),
]
