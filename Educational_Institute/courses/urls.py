from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from courses.views import SignupView , LoginView

urlpatterns = [
        path('', views.home, name='home'),
        path('signup', SignupView.as_view(), name='signup'),
        path('login',LoginView.as_view(), name='login'),
        path('logout', views.signout , name='logout'),
        path('mycourses', views.mycourses , name='mycourses'),           
        path('course/<str:slug>', views.coursePage, name='coursepage'),
        path('checkout/<str:slug>', views.checkout, name='checkout'),
        path('verify_payment', views.verify_payment, name='verify_payment'),
        
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)