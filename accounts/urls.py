from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/',views.signup, name='signup'),
    path('login/',views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('kakaocode/', views.kakao_code, name='kakaocode'),
    path('kakaologin/',views.kakao_signup, name='kakaosignup'),
    path('kakaokill/', views.kakao_del, name='kakaodel')
]
