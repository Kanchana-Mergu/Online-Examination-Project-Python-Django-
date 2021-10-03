from teacher.models import Marks, CirculateNotice, Course, ExamTimeTable, Exams, Questions, Results, Semester, Student
from django.db import models
from teacher.forms import AddExamTimeTableF, TeacherAddCourseF,TeacherAddSemF,TeacherAddStudentF,StudentUserForm,TeacherAddExamF,TeacherAddQuetionF,CirculateNoticeF
from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib.auth.decorators import login_required
from Exam import models as TMODEL
from student import forms as SFORM
from . import forms,models
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER
from datetime import date, datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
# Create your views here.
#def TeacherHome_view(request):
    #return render(request,'teacher/TeacherHome.html')

@login_required(login_url='login')
def teacher_dashboard_view(request):
    Teacherinfo=TMODEL.Teacher.objects.filter(user_id=request.user.id)
    notice=CirculateNotice.objects.all()
    TodaytotalExams=ExamTimeTable.objects.filter(Date=date.today())
    datewiseExamScheduledTotal=ExamTimeTable.objects.filter(Date=date.today(),Status='Scheduled')
    datewiseExamcompleted=ExamTimeTable.objects.filter(Date=date.today(),Status='End')
    datewiseExamActivated=ExamTimeTable.objects.filter(Date=date.today(),Status='Start')
    ActivatedExam=datewiseExamActivated.count()
    completedexam=datewiseExamcompleted.count()
    totalexam=datewiseExamScheduledTotal.count()
    todaytotalexam=TodaytotalExams.count()
    todayexamrunninglist=ExamTimeTable.objects.filter(Date=date.today(),Status='Start')
    #For Student
    srt=[]
    getcoursesemtoday=ExamTimeTable.objects.filter(Date=date.today()).distinct()
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
                    TotalStudentAllocated=Student.objects.filter(course=srt[temp1],semester=srt[temp])
                    stcount.append(TotalStudentAllocated.count())
                    temp=temp+2
                    temp1=temp1+2
    add=list(dict.fromkeys(stcount))# removing Duplicate Elements
    for ele in range(0,len(add)):
        totalst=totalst+add[ele]
    print(totalst)
    context={'todaytotalexam':todaytotalexam,'teacher':Teacherinfo,'notice':notice,'totalex':totalexam,'datewiseExam':datewiseExamScheduledTotal,'completed':completedexam,'examcomlist':datewiseExamcompleted,'activat':ActivatedExam,'examlist':todayexamrunninglist,'tstexam':totalst}
    return render(request,'teacher/TeacherDashboard.html',context)

#@login_required(login_url='login')
#def teacher_add_student(request):
#    return render(request,'teacher/AddStudent.html')

@login_required(login_url='login')
def teacher_manage_student(request):
    return render(request,'teacher/StudentDetails.html')
# View For Adding Course
@login_required(login_url='login')
def teacher_add_course(request):
    if request.method=='POST':
        courseobj=TeacherAddCourseF(request.POST)
        if courseobj.is_valid():
            cnm=courseobj.cleaned_data['course_name']
            if  Course.objects.filter(course_name=cnm).exists():
                messages.info(request,"Course Already Exists")
            else:
                cmobj=Course(course_name=cnm)
                cmobj.save()
                courseobj=TeacherAddCourseF()
                messages.info(request,"Course Added ")
    else:
        courseobj=TeacherAddCourseF()
    coursedetails=Course.objects.all()
    return render(request,'teacher/AddCourse.html',{'form':courseobj,'stu':coursedetails})
# Update Course
def update_course(request,id):
    if request.method=='POST':
        pi=Course.objects.get(pk=id)
        fm=TeacherAddCourseF(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi=Course.objects.get(pk=id)
        fm=TeacherAddCourseF(instance=pi)
    return render(request ,'teacher/UpdateCourse.html',{'form':fm})
#Delete Course
def delfun(request,pk):
    pi=Course.objects.get(id=pk)
    pi.delete()
    return HttpResponseRedirect('/teacher/teacher-addcourse')
            
# This View For Adding Semester
@login_required(login_url='login')
def teacher_add_semester(request):
    if request.method=='POST':
        courseobj=TeacherAddSemF(request.POST)
        if courseobj.is_valid():
            cnm=courseobj.cleaned_data['Sem']
            if Semester.objects.filter(Sem=cnm).exists():
                messages.info(request,"Semester Already Exists")
            else:
                cmobj=Semester(Sem=cnm)
                cmobj.save()
                courseobj=TeacherAddSemF()
                #print("Sem Added Successfully")
                messages.info(request,"Semester Added ")
    else:
        courseobj=TeacherAddSemF()
    semesterdetails=Semester.objects.all()
    return render(request,'teacher/AddSemester.html',{'form':courseobj,'stu':semesterdetails})

#This View For Student
@login_required(login_url='login')
def teacher_add_student(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.TeacherAddStudentF()
    students= Student.objects.all().filter(status=True)
    mydict={'userForm':userForm,'studentForm':studentForm,'students':students}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.TeacherAddStudentF(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
            email=userForm.cleaned_data['email']
            username=userForm.cleaned_data['username']
            passw=userForm.cleaned_data['password']
            '''send_mail(
            'Punyashlok Ahilyadevi Holkar Solapur University, Solapur (Online Exam Portal)',
            'This Student Name:'+username+'  And Password:'+passw+' Authentication For Your Online Examination...! Note: After Login Immediately Change Password',
            EMAIL_HOST_USER,
            [email],
            fail_silently=False,
                )'''
    return render(request,'teacher/AddStudent.html',context=mydict)
#View Student Details
@login_required(login_url='login')
def teacher_manage_student(request):
    studentdetails=Student.objects.all()
    return render(request,'teacher/StudentDetails.html',{'studentdetails':studentdetails})

# Update Student
def update_student(request,pk):
    Sstudent=Student.objects.get(id=pk)
    user=User.objects.get(id=Sstudent.user_id)
    userForm=StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=Sstudent)
    #mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=StudentUserForm(request.POST,instance=user)
        studentForm=TeacherAddStudentF(request.POST,request.FILES,instance=Sstudent)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
    else:
        student=Student.objects.get(id=pk)
        studentForm=TeacherAddStudentF(instance=student)
        user=User.objects.get(id=student.user_id)
        userForm=StudentUserForm(instance=user)
    return render(request ,'teacher/UpdateStudent.html',{'userForm':userForm,'studentForm':studentForm})

#Delete Student
def delstudent(request,id):
    pi=Student.objects.get(pk=id)
    pi.delete()
    return HttpResponseRedirect('/teacher/teacher-managestudent')
#View For Semester


# Update Semester
def update_semester(request,id):
    if request.method=='POST':
        pi=Semester.objects.get(pk=id)
        fm=TeacherAddSemF(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi=Semester.objects.get(pk=id)
        fm=TeacherAddSemF(instance=pi)
    return render(request ,'teacher/UpdateSemester.html',{'form':fm})

#Delete semester
def delsemester(request,id):
    pi=Semester.objects.get(pk=id)
    pi.delete()
    return HttpResponseRedirect('/teacher/teacher-addsem')
            
@login_required(login_url='login')
def teacher_add_exam(request):
    exobj=TeacherAddExamF()
    if request.method=='POST':
        exobj=forms.TeacherAddExamF(request.POST)
        if exobj.is_valid():
            exobj.save()
            exobj=TeacherAddExamF()
    else:
        exobj=TeacherAddExamF()
    return render(request,'teacher/AddExam.html',{'form':exobj})

@login_required(login_url='login')
def teacher_manage_exam(request):
    examdetails=Exams.objects.all()
    return render(request,'teacher/viewExams.html',{'stu':examdetails})

#Update Exam
@login_required(login_url='login')
def teacher_Update_exam(request,id):
    if request.method=='POST':
        pi=Exams.objects.get(pk=id)
        fm=TeacherAddExamF(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi=Exams.objects.get(pk=id)
        fm=TeacherAddExamF(instance=pi)
    return render(request,'teacher/UpdateExam.html',{'form':fm})


@login_required(login_url='login')
def delexam(request,id):
    pi=Exams.objects.get(Subject_code=id)
    pi.delete()
    return HttpResponseRedirect('/teacher/teacher-manageexam')

#Question Pepar
@login_required(login_url='login')
def teacher_upload_questionpepar(request):
    exobj=TeacherAddExamF()
    if request.method=='POST':
        exobj=forms.TeacherAddQuetionF(request.POST)
        if exobj.is_valid():
            exobj.save()
            exobj=TeacherAddQuetionF()
    else:
        exobj=TeacherAddQuetionF()
    return render(request,'teacher/UploadQuestions.html',{'form':exobj})

#View Question Pepar
@login_required(login_url='login')
def teacher_view_questionpepar(request):
    examdetails=Questions.objects.all()
    return render(request,'teacher/ViewQuestionsPepar.html',{'stu':examdetails})
#Update Question Paper
@login_required(login_url='login')
def teacher_Update_questionpepar(request,id):
    if request.method=='POST':
        pi=Questions.objects.get(pk=id)
        fm=TeacherAddQuetionF(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi=Questions.objects.get(pk=id)
        fm=TeacherAddQuetionF(instance=pi)
    return render(request,'teacher/UpdateQuetions.html',{'form':fm})

@login_required(login_url='login')
def AddExamTimeTable_view(request):
    exobj=AddExamTimeTableF()
    TimeTable=ExamTimeTable.objects.order_by('semester','course_name')
    Table=ExamTimeTable.objects.values('course_name','semester').distinct()
    lst=[entry for entry in Table]
    print(lst)
    list=[]
    for i in range(len(Table)):
        crs=Course.objects.get(id=Table[i]['course_name'])
        list.append(crs.course_name)
        sem=Semester.objects.get(id=Table[i]['semester'])
        list.append(sem.Sem)
    print(list)
    x = [list[i:i + 2] for i in range(0, len(list), 2)] 
    print(x) 
    for i in x:
        print(i[0],i[1])   
    if request.method=='POST':
        exobj=forms.AddExamTimeTableF(request.POST)
        if exobj.is_valid():
            exobj.save()
            exobj=AddExamTimeTableF()
    else:
        exobj=AddExamTimeTableF()
    return render(request,'teacher/AddExamTimeTable.html',{'form':exobj,'TimeTable':TimeTable,'x':x})

@login_required(login_url='login')
def Update_ExamTimeTable_view(request,id):
    if request.method=='POST':
        pi=ExamTimeTable.objects.get(pk=id)
        fm=AddExamTimeTableF(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi=ExamTimeTable.objects.get(pk=id)
        fm=AddExamTimeTableF(instance=pi)
    return render(request,'teacher/UpdateTimeTable.html',{'form':fm})

# Circulate Notice / Information 
@login_required(login_url='login')
def teacher_circulate_notice(request):
    notice=CirculateNotice.objects.all()
    return render(request,'teacher/CirculateInformation.html',{'notice':notice})

# Circulated Notice / Update Information
@login_required(login_url='login')
def teacher_update_circulate_notice(request,id):
    if request.method=='POST':
        pi=CirculateNotice.objects.get(pk=id)
        fm=CirculateNoticeF(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi=CirculateNotice.objects.get(pk=id)
        fm=CirculateNoticeF(instance=pi)
    return render(request,'teacher/UpdateNotice.html',{'form':fm})

@login_required(login_url='login')
def teacher_studentgivenexam_view(request):
    try:
        flag=[]
        demo=Marks.objects.all()
        for d in demo:
            studentdetails=Student.objects.filter(id=d.student_id)
            for st in studentdetails:
                flag.append(st.profile_pic)              
        zippedlist=zip(demo,flag)
    except ObjectDoesNotExist:
        return HttpResponse("Exception: Data not found")  
    context={'zip':zippedlist}
    return render(request,'teacher/Viewstudentgivenexam.html',context)

@login_required(login_url='login')
def teacher_checkexam_view(request,id,code):
    try:
        demo=Results.objects.filter(student=id,papercode=code)
        que=Questions.objects.filter(Paper_code=code).order_by('question_id')
        list=zip(demo,que)
    except ObjectDoesNotExist:
        return HttpResponse("Exception: Data not found")  
    return render(request,'teacher/CheckExam.html',{'list':list})

# Generate Result PDF 
@login_required(login_url='login')
def teacher_generate_result(request):
    return render(request,'teacher/GenerateResultsPDF.html')