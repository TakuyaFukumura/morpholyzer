from django.urls import path
from . import views

app_name = 'morpholyzer'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/analyze/', views.api_analyze, name='api_analyze'),
]
