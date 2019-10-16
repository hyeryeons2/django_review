from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # create url 만들기
    path('create/', views.create, name='create'),
]