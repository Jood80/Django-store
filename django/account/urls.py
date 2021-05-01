from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path("csrf/", views.get_csrf, name="api_csrf"),
    path('login/', views.login_view, name='api_login'),
  ]
