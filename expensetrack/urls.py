from django.urls import path
from . import views

urlpatterns = [
    path('update/<int:id>', views.update, name = 'update'),
    path('delete/<int:id>', views.delete, name = 'delete'),
# ----------------------------------------------------------------------
    path('elements/', views.elements, name = 'elements'),
# ----------------------------------------------------------------------
    path('myreport/', views.myreport, name = 'myreport'),
# ----------------------------------------------------------------------
    path('about/', views.about, name = 'ABOUT'),
    path('contact/', views.contact, name = 'CONTACT'),
    path('', views.index, name = 'INDEX'),
    path('innerpage/', views.innerpage, name = 'INNERPAGE'),
    path('portfolio/', views.portfolio, name = 'PORTFOLIO'),
    path('portfoliodetails/', views.portfoliodetails, name = 'PORTFOLIODETAILS'),
    path('pricing/', views.pricing, name = 'PRICING'),
    path('services/', views.services, name = 'SERVICES'),
    path('faq/', views.faq, name = 'FAQ'),
    path('team/', views.team, name = 'TEAM'),
    path('testimonials/', views.testimonials, name = 'TESTIMONIALS'),
    path('signup/', views.signup, name = 'SIGNUP'),
    path('login/', views.login, name = 'LOGIN'),
    path('logout/', views.userLogOut, name = 'LOGOUT'),
# ----------------------------------------------------------------------
    path('add_category/', views.add_category, name = 'add_category'),
    path('allexpense/', views.ALL_EXPENSE, name = 'ALL_EXPENSE'),
# ----------------------------------------------------------------------
    path('add_expense/', views.add_expense, name = 'add_expense'),
    
# ----------------------------------------------------------------------
]