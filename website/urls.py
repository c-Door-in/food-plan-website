from django.urls import path
from .views import mainpage, cardpage


urlpatterns = [
    path('', mainpage),
    path('card/', cardpage)
]

