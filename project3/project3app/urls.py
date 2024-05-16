from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:number>',views.printNumber, name='printNumber'),
    path('<str:string>',views.printString, name='printString'),

    path('login/', views.loginIndex, name='loginIndex'),
    path('login/#', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('player_home/', views.player_home, name='player_home'),
    path('coach_home/', views.coach_home, name='coach_home'),
    path('jury_home/', views.jury_home, name='jury_home'),
]