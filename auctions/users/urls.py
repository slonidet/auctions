from django.conf.urls import url

from . import views


urlpatterns = [
    url('register', views.UserCreateView.as_view(), name='user-registrate'),
    url('login', views.AuthTokenView.as_view(), name='login')
]
