from django.urls import path
from . import views

urlpatterns = [
    path('add_comparison/', views.add_comparison, name='add_comparison'),
    path('get_session_pair/', views.get_session_pair, name='get_session_pair'),
]
