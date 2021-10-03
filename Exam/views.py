from django.core.checks import messages
from django.core.mail.message import EmailMessage
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from . import forms,models
from django.http import HttpResponseRedirect
from Exam import models as TMODEL
from teacher import models as SMODEL
from django.conf.global_settings import EMAIL_HOST_USER
from datetime import date, datetime
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

# Create your views here.
def Home_View(request):
    return render(request,'Exam/Home.html')

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "Exam/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'akdemo00@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="Exam/password_reset.html", context={"password_reset_form":password_reset_form})

def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_student(request.user):      
        return redirect('student/student-dashboard')
                
    elif is_teacher(request.user):
            return redirect('teacher/teacher-dashboard')
        
    else:
        return redirect('admin-dashboard')

@login_required(login_url='login')
def admin_dashboard_view(request):
    notice=SMODEL.CirculateNotice.objects.all()
    Teacherinfo=TMODEL.Teacher.objects.filter(user_id=request.user.id)
    notice=SMODEL.CirculateNotice.objects.all()
    TodaytotalExams=SMODEL.ExamTimeTable.objects.filter(Date=date.today())
    datewiseExamScheduledTotal=SMODEL.ExamTimeTable.objects.filter(Date=date.today(),Status='Scheduled')
    datewiseExamcompleted=SMODEL.ExamTimeTable.objects.filter(Date=date.today(),Status='End')
    datewiseExamActivated=SMODEL.ExamTimeTable.objects.filter(Date=date.today(),Status='Start')
    ActivatedExam=datewiseExamActivated.count()
    completedexam=datewiseExamcompleted.count()
    totalexam=datewiseExamScheduledTotal.count()
    todaytotalexam=TodaytotalExams.count()
    todayexamrunninglist=SMODEL.ExamTimeTable.objects.filter(Date=date.today(),Status='Start')
    #For Student
    srt=[]
    getcoursesemtoday=SMODEL.ExamTimeTable.objects.filter(Date=date.today()).distinct()
    for dt in getcoursesemtoday:
        srt.append(dt.course_name) 
        srt.append(dt.semester) 
    temp=1
    temp1=0
    totalst=0
    stcount=[]
    for st in range(0,len(srt)):
           local=len(srt)+1
           if temp!=local:
                if temp1!=temp:
                    TotalStudentAllocated=SMODEL.Student.objects.filter(course=srt[temp1],semester=srt[temp])
                    stcount.append(TotalStudentAllocated.count())
                    temp=temp+2
                    temp1=temp1+2
    add=list(dict.fromkeys(stcount))# removing Duplicate Elements
    for ele in range(0,len(add)):
        totalst=totalst+add[ele]
    print(totalst)
    context={'todaytotalexam':todaytotalexam,'teacher':Teacherinfo,'notice':notice,'totalex':totalexam,'datewiseExam':datewiseExamScheduledTotal,'completed':completedexam,'examcomlist':datewiseExamcompleted,'activat':ActivatedExam,'examlist':todayexamrunninglist,'tstexam':totalst}
    return render(request,'Exam/AdminDashboard.html',context)

@login_required(login_url='login')
def admin_add_faculty_view(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    teachers= TMODEL.Teacher.objects.all()
    if request.method=='POST':
        em=request.POST.get('email')
        unm=request.POST.get('username')
        fn=request.POST.get('first_name')
        ln=request.POST.get('last_name')
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if User.objects.filter(email=em).exists():            
            messages.info(request,"This email already exists.")
            print("email Exists")
        elif User.objects.filter(username=unm).exists():            
            messages.info(request,"This username already exists.")
            print("username Exists")
        elif User.objects.filter(first_name=fn,last_name=ln):
            messages.info(request,"This First name and Last name already exists.")
            print("first name and last name exists.")
        elif User.objects.filter(first_name=fn,last_name=ln,email=em,username=unm):
            messages.info(request,"This Faculty already exists.")
        else:
            print("Not exists")
            if userForm.is_valid() and teacherForm.is_valid():
                user=userForm.save()
                user.set_password(user.password)
                user.save()
                teacher=teacherForm.save(commit=False)
                teacher.user=user
                teacher.save()
                my_teacher_group = Group.objects.get_or_create(name='TEACHER')
                my_teacher_group[0].user_set.add(user)
                messages.info(request,"Faculty Added and email sent successfully.")
                email=userForm.cleaned_data['email']
                username=userForm.cleaned_data['username']
                passw=userForm.cleaned_data['password']
                send_mail(
                'Punyashlok Ahilyadevi Holkar Solapur University, Solapur',
                'This Faculty Name:'+username+'  And Password:'+passw+' Authentication For Your Staff ...! And Welcome To Our University',
                 EMAIL_HOST_USER,
                 [email],
                 fail_silently=False,
                      )
    mydict={'userForm':userForm,'teacherForm':teacherForm,'teachers':teachers}
    return render(request,'Exam/AddFaculty.html',context=mydict)

#Student Details
@login_required(login_url='login')
def admin_manage_student(request):
    studentdetails=SMODEL.Student.objects.all()
    return render(request,'Exam/StudentDetails.html',{'studentdetails':studentdetails})
#Student Details
@login_required(login_url='login')
def admin_view_examtimetable(request):
    TimeTable=SMODEL.ExamTimeTable.objects.order_by('semester','course_name')
    return render(request,'Exam/ExamTimeTable.html',{'TimeTable':TimeTable})
