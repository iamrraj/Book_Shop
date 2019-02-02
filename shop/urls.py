from django.urls import path
from . import views

#from .views import (BlogDetailView)

urlpatterns = [

    path('', views.index, name='index'),
]

