from django.urls import path,include
from .import views
from django.conf import settings

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.loginpage,name='login'),
    path('signup/',views.signuppage,name='signup'),
    path('forgetpassword/',views.forgetpassword,name='forgetpassword'),
    path('resetpassword/<token>/',views.resetpassord,name='resetpassord'),
    path('scrape_data/',views.scrapedata,name='scrape'),


 ]

