from django import forms
from django.contrib.auth.models import User
from django.db.models.fields import Field
from django.forms import widgets
from teacher.models import Student,ExamTimeTable
class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','password']
        widgets = {
        'password':forms.PasswordInput(),
        }
   
class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['profile_pic','mobile_no']
        
class ExamTimeTableForm(forms.ModelForm):
    class Meta:
        model=ExamTimeTable
        fields=['Date','course_name','semester','Paper_code','Subject','FromTime','ToTime','Status']
