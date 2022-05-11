from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name = 'index'),
    path('add', views.add, name = 'add'),
    path('update/<int:id>', views.update, name = 'update'),
    path('delete/<int:id>', views.delete, name = 'delete'),
# ----------------------------------------------------------------------
    path('report/', views.report, name = 'report'),
    path('myreport/', views.myreport, name = 'myreport'),
# ----------------------------------------------------------------------
    path('', views.index, name = 'INDEX'),
    path('about/', views.about, name = 'ABOUT'),
    path('contact/', views.contact, name = 'CONTACT'),
    path('signup/', views.signup, name = 'SIGNUP'),
    path('login/', views.login, name = 'LOGIN'),
    path('logout/', views.userLogOut, name = 'LOGOUT'),
    
    path('expense/', views.expense, name = 'expense'),

]