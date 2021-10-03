from re import template
from django.contrib.auth.views import LoginView
from django.urls import path
from django.urls.resolvers import URLPattern
from.import views
from django.contrib.auth.views import LoginView
urlpatterns=[
   # path('',views.TeacherHome_view,name='teacherhome'),
    #path('teacherlogin/',LoginView.as_view(template_name='teacher/TeacherLogin.html'),name='teacherlogin'),
    path('teacher-dashboard/',views.teacher_dashboard_view,name='teacher-dashboard'),
    path('teacher-addstudent/',views.teacher_add_student,name='teacher-addstudent'),
    path('teacher-managestudent/',views.teacher_manage_student,name='teacher-managestudent'),
    path('student/<int:pk>/',views.update_student,name='teacher-updatestudent'),
    path('delstud/<int:id>/', views.delstudent,name="Delete"),
    path('teacher-addcourse/',views.teacher_add_course,name='teacher-addcourse'),
    path('teacher-addsem/',views.teacher_add_semester,name='teacher-addsem'),
    path('<int:id>/',views.update_course,name='teacher-updatecourse'),
    path('semester/<int:id>/',views.update_semester,name='teacher-updatesemester'),
    path('delsem<int:id>/', views.delsemester,name="delsem"),
    path('delcrs/<int:pk>/', views.delfun,name="delcrs"),
    path('teacher-addexam/',views.teacher_add_exam,name='teacher-addexam'),
    path('teacher-addquestionspepar/',views.teacher_upload_questionpepar,name='teacher-addquestionspepar'),
    path('teacher-viewquestionspepar/',views.teacher_view_questionpepar,name='teacher-viewquestionspepar'),
    path('Question/<int:id>/',views.teacher_Update_questionpepar,name='teacher-updatequestions'),
    path('teacher-manageexam/',views.teacher_manage_exam,name='teacher-manageexam'),
    path('Exam/<int:id>/',views.teacher_Update_exam,name='teacher-updateexam'),
    path('deletexam/<int:id>/', views.delexam,name="deletexam"),
    path('add-exam-timetable',views.AddExamTimeTable_view,name='add-exam-timetable'),
    path('update-timetable/<int:id>',views.Update_ExamTimeTable_view,name='update-timetable'),
    path('teacher-circulate-notice/',views.teacher_circulate_notice,name='teacher-circulate-notice'),
    path('updatenotice/<int:id>',views.teacher_update_circulate_notice,name='updatenotice'),
    path('view-given-exam/',views.teacher_studentgivenexam_view,name='view-given-exam'),
    path('check-exam/<id>/<code>/',views.teacher_checkexam_view,name='check-exam'),
    path('Generate-result',views.teacher_generate_result,name='Generate-result'),    
]