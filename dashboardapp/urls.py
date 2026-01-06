
from django.urls import path

from dashboardapp import views


urlpatterns = [
    path('', views.HomePage,name='home'),
    path('machine/<int:machine_id>/config/', views.machine_config, name='machine_config'),
    # path('homepage/', views.HomePage,name='home'),
]