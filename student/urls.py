from re import template
from django.urls import path
from django.urls.resolvers import URLPattern
from student import views
from django.contrib.auth.views import LoginView

urlpatterns=[
    #path('',views.StudentHome_View),
    #path('studentlogin/', LoginView.as_view(template_name='student/StudentLogin.html'),name='studentlogin'),
    path('student-dashboard/', views.student_dashboard_view,name='student-dashboard'),
    path('student-profile/',views.student_profile_view,name='student-profile'),
    path('student-update-profile/<int:pk>/',views.student_update_view,name='student-update-profile'),
    path('student-load-pepar<int:Paper_code>/',views.Student_load_pepar,name='student-load-pepar'),
    path('student-examsubmit/',views.Student_exam_submitted,name='student-examsubmit'),
    path('student-view-marks/',views.Student_view_marks,name='student-view-marks'),
    path('view-exam-marks/<id>/<code>/',views.Student_view_exammarks,name='view-exam-marks'),  
  ]