from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model, ModelBase
from django.db.models.fields import CommaSeparatedIntegerField, IntegerField
from django.forms.utils import to_current_timezone

# Create your models here.
class Course(models.Model):
    course_name=models.CharField(max_length=50)
    def __str__(self):
        return u'{0}'.format(self.course_name)

#Model For Semester
class Semester(models.Model):
    Sem=models.CharField(max_length=10)
    def __str__(self):
        return u'{0}'.format(self.Sem)

#Model For Student
class Student(models.Model):
     seat_no=models.IntegerField()
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     course=models.ForeignKey(Course,on_delete=models.CASCADE)
     semester=models.ForeignKey(Semester,on_delete=models.CASCADE)
     mobile_no=models.IntegerField(max_length=10,null=False)
     profile_pic=models.ImageField(upload_to='profile_pic/Student/',null=True,blank=True)
     status=models.BooleanField(default=True)
     def __str__(self):
        return u'{0}'.format(self.user.id)

#Model For Exam
class Exams(models.Model):
    Subject_code=models.CharField(primary_key=True,max_length=10,null=False)
    Subject_name=models.CharField(max_length=100,null=False)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    semester=models.ForeignKey(Semester,on_delete=models.CASCADE)
    Duration=IntegerField(max_length=10,default=30)
    marks=IntegerField(max_length=100,null=False)
    Exammonth=models.CharField(max_length=10,null=False,default='oct')
    Examyear=models.IntegerField(max_length=10,default=2021)
    def __str__(self):
        return u'{0}'.format(self.Subject_code)

#Model for Exam Time table
STATUS_CHOICES=(("Scheduled","Scheduled"),("Start","Start"),("End","End"))
class ExamTimeTable(models.Model):
    course_name=models.ForeignKey(Course,on_delete=models.SET_NULL,null=True)
    semester=models.ForeignKey(Semester,on_delete=models.SET_NULL,null=True)
    Date=models.DateField()
    #Paper_code=models.ForeignKey(Exams,on_delete=models.SET_NULL,null=True)
    Paper_code=models.CharField(max_length=20,null=False)
    Subject=models.CharField(max_length=20,null=False)
    FromTime=models.TimeField(auto_now=False,auto_now_add=False)
    ToTime=models.TimeField(auto_now=False,auto_now_add=False)
    Status=models.CharField(max_length=20,null=False,choices=STATUS_CHOICES,default='Scheduled')

class Questions(models.Model):
    question_id=models.IntegerField()
    Paper_code=models.ForeignKey(Exams,on_delete=models.CASCADE)
    question=models.CharField(max_length=300,null=False)
    Option1=models.CharField(max_length=200,null=False)
    Option2=models.CharField(max_length=200,null=False)
    Option3=models.CharField(max_length=200,null=False)
    Option4=models.CharField(max_length=200,null=False)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)
    marks=models.PositiveIntegerField()
    #Correct_ans=models.CharField(max_length=200)

class Results(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    seatno=models.IntegerField()
    papercode=models.CharField(max_length=20,null=False)
    questionid=models.CharField(max_length=50,null=False)
    correctanswer=models.CharField(max_length=100,null=False)
    selectedanswer=models.CharField(max_length=100,null=False)
    questionmarks=models.IntegerField(max_length=100,null=False)
    obtainedmarks=models.IntegerField(max_length=100,null=False)
    Date=models.DateField()
    Status=models.CharField(max_length=20,null=False)

class Marks(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    seatno=models.IntegerField()
    course_name=models.CharField(max_length=100,null=False)
    semester=models.CharField(max_length=100,null=False)
    Subject_name=models.CharField(max_length=100,null=False)
    papercode=models.CharField(max_length=100,null=False)
    Totalmarks=models.PositiveIntegerField()
    obtainedmarks=models.PositiveIntegerField()
    date = models.DateField()
  
class CirculateNotice(models.Model):
    NoticeForStudentloginPage=models.CharField(max_length=300,null=True)
    NoticeForStudentExamTimeTable=models.CharField(max_length=300,null=True)
    NoticeForStudentQuestionPeparLoad=models.CharField(max_length=300,null=True)
    NoticeForEveryOnearjunt=models.CharField(max_length=300,null=True)
    
'''class Course(models.Model):
    course_name=models.CharField(max_length=50,default=0)
    def __str__(self):
        return u'{0}'.format(self.course_name)

class Sem(models.Model):
    semester=models.CharField(max_length=50,default=0)
    def __str__(self):
        return u'{0}'.format(self.semester)

class Student(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    course_name=models.ForeignKey(Course,on_delete=models.SET_NULL,null=True)
    semester=models.ForeignKey(Sem,on_delete=models.SET_NULL,null=True)
    SeatNo=models.IntegerField(default=False,null=False)
    profile_pic=models.ImageField(upload_to='profile_pic/Student/',null=True,blank=True)
    address=models.CharField(max_length=40)
    mobile=models.CharField(max_length=20,null=False)
    status=models.BooleanField(default=False)'''



