from django.urls import path
from . import views

urlpatterns = [
    path('my_api/', views.MyView.as_view()),
]