from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('<int:article_pk>/delete/', views.delete, name='delete'),
    path('<int:article_pk>/update/', views.update, name='update'),
    path('<int:article_pk>/', views.detail, name='detail'),
    path('', views.index, name='index'),
    # create url 만들기
    path('create/', views.create, name='create'),
]