from django.contrib.auth.models import User
from django.db.models.fields import SmallIntegerField
from django.http import response
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from student import forms as SFORM
from teacher import models as SMODEL
from datetime import datetime
from django.db.models.functions.datetime import ExtractDay, ExtractHour, ExtractMinute, ExtractMonth, ExtractSecond, ExtractYear
from django.db.models.functions import Extract
from django.utils import timezone

# Create your views here.
#This function will login student
#def StudentHome_View(request):
 #   return render(request,'student/StudentHome.html')

@login_required(login_url='login')
def student_dashboard_view(request):
    Studentinfo=SMODEL.Student.objects.filter(user_id=request.user.id)
    for table in Studentinfo:
        id=table.id
        crs=table.course
        sm=table.semester       
    ExamTime=SMODEL.ExamTimeTable.objects.filter(course_name=crs,semester=sm)
    flag=[]
    for time in ExamTime:
        ex=SMODEL.Marks.objects.filter(student=id,course_name=time.course_name,semester=time.semester,papercode=time.Paper_code)
        if ex:
            flag.append(1)
        else:
            flag.append(0)
    print(flag)
    zipedlist=zip(ExamTime,flag)
    context={'student':Studentinfo,'examtime':ExamTime,'zip':zipedlist}
    return render(request,'student/StudentDashboard.html',context)
@login_required(login_url='login')
def student_profile_view(request):
    Studentuser=SMODEL.User.objects.filter(id=request.user.id)
    Studentinfo=SMODEL.Student.objects.filter(user_id=request.user.id)
    context={'user':Studentuser,'student':Studentinfo}
    return render(request,'student/StudentProfile.html',context)

#@login_required(login_url='login')
def student_update_view(request,pk):
    Sstudent=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=Sstudent.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=Sstudent)
    #mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=Sstudent)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('student-profile')
    else:
        student=SMODEL.Student.objects.get(id=pk)
        studentForm=SFORM.StudentForm(instance=Sstudent)
        user=SMODEL.User.objects.get(id=Sstudent.user_id)
        userForm=SFORM.StudentUserForm(instance=user)
    return render(request,'student/StudentProfileUpdate.html',{'userForm':userForm,'studentForm':studentForm,'Sstudent':Sstudent,'user':user})


@login_required(login_url='login')
def Student_load_pepar(request,Paper_code):
    if request.method=='POST':
        exdetails=SMODEL.ExamTimeTable.objects.filter(Paper_code=Paper_code)
        papercode=SMODEL.Questions.objects.filter(Paper_code=Paper_code)  
    else:
        papercode=SMODEL.Questions.objects.filter(Paper_code=Paper_code).order_by('question_id')
        exdetails=SMODEL.ExamTimeTable.objects.filter(Paper_code=Paper_code)
        loaddurationm=SMODEL.Exams.objects.filter(Subject_code=Paper_code)
        notice=SMODEL.CirculateNotice.objects.all()
        papercodeconvertinto=list(papercode)
        qlist=[]
        print(papercode)
        for questions in papercode:
            print(questions.question)
            que=questions.question
            q=que.replace(",",".")
            print(q)
            qlist.append(questions.question_id)
            qlist.append(q)
            qlist.append(questions.Option1)
            qlist.append(questions.Option2)
            qlist.append(questions.Option3)
            qlist.append(questions.Option4)
    print(qlist)
    response=render(request,'student/LoadPepar.html',{'code':qlist,'exdetail':exdetails,'loaddum':loaddurationm,'notice':notice})
    response.set_cookie('Paper_code',Paper_code)
    return response

@login_required(login_url='login')
def Student_exam_submitted(request):  
    if 'answers' in request.POST:
        allanswers=request.POST['answers']
        answers=allanswers.split(",")
        anslist=[]
        for ans in answers:
            a=ans.replace(" ","")
            anslist.append(a)
        if request.COOKIES.get('Paper_code') is not None:
            code=request.COOKIES.get('Paper_code')
            papercode=SMODEL.Questions.objects.all().filter(Paper_code=code)
            Optionlist=[]
            for ans in papercode:
                Qid=ans.question_id
                Options=ans.answer
                mark=ans.marks
                Optionlist.append(Qid)
                Optionlist.append(Options)
                Optionlist.append(mark)
        x = [anslist[i:i + 2] for i in range(0, len(anslist), 2)] 
        y=[Optionlist[i:i + 3] for i in range(0, len(Optionlist), 3)] 
        student=SMODEL.Student.objects.get(user_id=request.user.id)
        stno=student.seat_no
        totalmarks=0
        result=SMODEL.Results()
        #Saving in Result table
        for i,j in zip(x,y):
            if str(i[0]==j[0]):
                if i[1]==j[1]:
                    totalmarks+=j[2]
                    result.pk=None
                    result.student=student
                    result.seatno=stno
                    result.papercode=code
                    result.questionid=i[0]
                    result.correctanswer=j[1]
                    result.selectedanswer=i[1]
                    result.questionmarks=j[2]
                    result.obtainedmarks=j[2]
                    result.Date=datetime.now().strftime('%Y-%m-%d')
                    result.Status="correct"
                    result.save()
                else: 
                    result.pk=None
                    result.student=student
                    result.seatno=stno
                    result.papercode=code
                    result.questionid=i[0]
                    result.correctanswer=j[1]
                    result.selectedanswer=i[1]
                    result.questionmarks=j[2]
                    result.obtainedmarks=0
                    result.Date=datetime.now().strftime('%Y-%m-%d')
                    result.Status="wrong"
                    result.save()  
        #Calculating marks and saving into Marks table  
        exam=SMODEL.Exams.objects.get(Subject_code=code)
        Mark=SMODEL.Marks()
        Mark.pk=None
        Mark.student=student
        Mark.seatno=stno
        Mark.course_name=exam.course
        Mark.semester=exam.semester
        Mark.Subject_name=exam.Subject_name
        Mark.papercode=exam.Subject_code
        Mark.Totalmarks=exam.marks
        Mark.obtainedmarks=totalmarks
        Mark.date=datetime.now().strftime('%Y-%m-%d')
        Mark.save()
    else:
        allanswers=False
    return render(request,'student/ShowExamSubmitted.html')

@login_required(login_url='login')
def Student_view_marks(request):
    student=SMODEL.Student.objects.get(user_id=request.user.id)
    print(student.id)
    print(student.course)
    print(student.semester)
    marks=SMODEL.Marks.objects.filter(student=student.id,course_name=student.course,semester=student.semester)
    return render(request,'student/StudentViewMarks.html',{'Std':student,'studentmarks':marks})
 
@login_required(login_url='login')
def Student_view_exammarks(request,id,code):
    demo=SMODEL.Results.objects.filter(student=id,papercode=code)
    que=SMODEL.Questions.objects.filter(Paper_code=code).order_by('question_id')
    list=zip(demo,que)  
    return render(request,'student/ViewExamMarks.html',{'list':list})

   