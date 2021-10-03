from django.contrib import admin
from Exam.models import Teacher

# Register your models here.
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display=('id','profile_pic','mobile','status')