from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # 좋아요
    path('<int:article_pk>/like/', views.like, name='like'),

    path('<int:article_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),

    # comment url 만들기
    path('<int:article_pk>/comments/', views.comments_create, name='comments_create'),

    path('<int:article_pk>/delete/', views.delete, name='delete'),
    path('<int:article_pk>/update/', views.update, name='update'),
    path('<int:article_pk>/', views.detail, name='detail'),
    path('', views.index, name='index'),
    # create url 만들기
    path('create/', views.create, name='create'),
]