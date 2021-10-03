"""OnlineExam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from collections import namedtuple
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
from Exam import views
from django.contrib.auth import views as auth_views #import this
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home_View,name=''),
    path('login/',LoginView.as_view(template_name='Exam/Login.html'),name='login'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('admin-dashboard/', views.admin_dashboard_view,name='admin-dashboard'),
    path('add-faculty/',views.admin_add_faculty_view,name='add-faculty'),
    path('admin-viewstudent/',views.admin_manage_student,name='admin-viewstudent'),
    path('admin-viewsExamTimeTable/',views.admin_view_examtimetable,name='admin-viewsExamTimeTable'),
    #path('teacher-register/',views.teacher_register_view,name='teacher-register'),
    path('logout/',LogoutView.as_view(template_name='Exam/Logout.html'),name='studentlogout'),
    path('teacher/',include('teacher.urls')),
    path('student/',include('student.urls')),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Exam/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="Exam/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='Exam/password_reset_complete.html'), name='password_reset_complete'),      
]
