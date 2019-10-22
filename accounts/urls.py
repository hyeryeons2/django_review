from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # django에서는 회원정보 수정 시 비번 수정 기능을 제공하지 않기에 password를 따로 구현해야 함
    path('password/', views.password, name='password'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]
