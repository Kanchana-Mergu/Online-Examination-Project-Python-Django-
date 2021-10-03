from Exam import models
from django.contrib import admin
from teacher.models import ExamTimeTable, Marks, Semester,Student,Exams,Course,Questions,Results,CirculateNotice

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display=('seat_no','course','semester','mobile_no','profile_pic','status')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=('id','course_name')

@admin.register(Semester)
class SemAdmin(admin.ModelAdmin):
    list_display=('id','Sem')

@admin.register(Exams)
class ExamAdmin(admin.ModelAdmin):
    list_display=('Subject_code','Subject_name','course','semester','Duration','marks','Exammonth','Examyear')

@admin.register(ExamTimeTable)
class ExamTimeAdmin(admin.ModelAdmin):
    list_display=('course_name','semester','Date','Paper_code','Subject','FromTime','ToTime','Status')

@admin.register(Questions)
class QuestionsList(admin.ModelAdmin):
    list_display=('question_id','Paper_code','question','Option1','Option2','Option3','Option4','answer')

@admin.register(Results)
class Result(admin.ModelAdmin):
    list_display=('student','seatno','papercode','questionid','correctanswer','selectedanswer','questionmarks','obtainedmarks','Date','Status')

@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display=('student','seatno','course_name','semester','Subject_name','papercode','Totalmarks','obtainedmarks','date')

@admin.register(CirculateNotice)
class Notice(admin.ModelAdmin):
    list_display=('NoticeForStudentloginPage','NoticeForStudentExamTimeTable','NoticeForStudentQuestionPeparLoad','NoticeForEveryOnearjunt')