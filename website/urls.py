from django.urls import path

from . import views


urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('order/', views.order, name='order'),
    path('card/<int:pk>', views.CardView.as_view(), name='card'),
    path('subscribe/<int:pk>', views.subscribe, name='subscribe'),
    path('wrongtime/', views.wrongtime, name='wrongtime'),
]

