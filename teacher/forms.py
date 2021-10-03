from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django import forms
from django.forms import fields, widgets
from django.shortcuts import render
from .import models

# Thsi Form For Adding Course 
class TeacherAddCourseF(forms.ModelForm):
      class Meta:
          model=models.Course
          fields=['course_name']
# Thsi Form For Adding Semester
class TeacherAddSemF(forms.ModelForm):
      class Meta:
          model=models.Semester
          fields=['Sem']
#This for For Adding New Student
class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email']
        widgets = {
        'password': forms.PasswordInput(render_value=True),
         }
class TeacherAddStudentF(forms.ModelForm):
      class Meta:
          model=models.Student
          fields=['seat_no','course','semester','mobile_no','profile_pic','status']

class TeacherAddExamF(forms.ModelForm):
      class Meta:
          model=models.Exams
          fields=['Subject_code','Subject_name','course','semester','Duration','marks','Exammonth','Examyear']
         
class TeacherAddQuetionF(forms.ModelForm):
      class Meta:
          model=models.Questions
          fields=['question_id','Paper_code','marks','question','Option1','Option2','Option3','Option4','answer']
          widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }

class AddExamTimeTableF(forms.ModelForm):
    class Meta:
        model=models.ExamTimeTable
        fields=['course_name','semester','Date','Paper_code','Subject','FromTime','ToTime','Status']
class CirculateNoticeF(forms.ModelForm):
    class Meta:
        model=models.CirculateNotice
        fields=['NoticeForStudentloginPage','NoticeForStudentExamTimeTable','NoticeForStudentQuestionPeparLoad','NoticeForEveryOnearjunt']
