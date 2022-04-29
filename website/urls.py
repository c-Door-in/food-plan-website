from django.urls import path

from website.views import mainpage, CardView


urlpatterns = [
    path('', mainpage, name='mainpage'),
    path('card/<int:pk>', CardView.as_view(), name='card-detail')
]

