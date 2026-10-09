
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import*
from datetime import datetime
from django.contrib.auth.decorators import login_required
import csv


from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.apps import apps

from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.apps import meet_v2

import json



# Google Meet integration lives in google_meet.py; keep URL-facing names here.
from .google_meet import (
    google_login, google_callback, schedule_meeting, start_meeting,
    student_classes, join_meeting, teacher_meetings, superadmin_meetings,
)
from .models import GoogleMeeting





from django.views.decorators.cache import cache_control
from .compiler_helper import LANGUAGES, STARTER_CODE, run_code
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.cache import cache_control
from .compiler_helper import LANGUAGES, STARTER_CODE, run_code



# Create your views here.

'''////////////////////////////////// Login ////////////////////////////////////'''

def Home(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(
            username=username,
            password=password
        )
        
        if user is not None:
            login(request,user)
            if user.is_superuser:
                messages.success(request,"Login Successfully")
                return redirect("superadmindash")
            elif hasattr(user,"Teacher"):
                messages.success(request,"Login Successfully")
                return redirect('teacherdash')
            elif hasattr(user,"Student"):
                messages.success(request,"Login Successfully")
                return redirect('studentdash')
            else:
                messages.error(request,"You Are Not Authorized")
        else:
            messages.error(request,"Username & Password is Incorrect, Please try again")

    return render(request,'superadmin/login.html')



'''/////////////////////////// Superadmin Zone ////////////////////////////'''

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def superadmindash(request):
    student=AddStudent.objects.all()
    students=student.count()
    session=AddSession.objects.all()
    sessions=session.count()
    course=AddCourse.objects.filter(status="Active")
    courses=course.count()
    onlineclass=GoogleMeeting.objects.filter(status="scheduled")
    classes=onlineclass.count()
    teacher=AddTeacher.objects.all()
    teachers=teacher.count()
    subject=AddSubject.objects.filter(status="Active")
    subjects=subject.count()
    assignment=AddTask.objects.filter(status="Published")
    assignments=assignment.count()
    test=Test.objects.filter(status="Published")
    tests=test.count()
    return render(request,"superadmin/dashboard.html",{"students":students,"sessions":sessions,"courses":courses,"classes":classes,"teachers":teachers,"subjects":subjects,"assignments":assignments,"tests":tests})

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def add_session(request):
    if request.method=="POST":
        session_name=request.POST.get('session_name')
        if AddSession.objects.filter(session_name=session_name).exists():
            messages.error(request, "This session already exists!")
        else: 
            AddSession.objects.create(
                session_name=session_name,
                status=request.POST.get('status'),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                Dor=datetime.now()    
        )
            messages.success(request,"Session added successfully")
    return render(request,'superadmin/add_session.html',{'page_title':'Add Session'})

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def show_session(request):
    ab=AddSession.objects.all()
    return render(request, 'superadmin/show_session.html',{'ab':ab,'page_title':'Show Sessions'})

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def edit_session(request,id):
    s=AddSession.objects.get(id=id)
    if request.method == "POST":
        s.session_name = request.POST.get('session_name')
        s.status=request.POST.get('status')
        s.start_date=request.POST.get('start_date')
        s.end_date=request.POST.get('end_date')
        s.save()
        messages.success(request,'Session updated successfully')
        return redirect('show_session')
    return render(request,'superadmin/edit_session.html',{'s':s})

def delete_session(request,id):
    s=AddSession.objects.get(id=id)
    s.delete()
    messages.success(request,'Session deleted successfully')
    return redirect('show_session')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def add_course(request):
    session_data=AddSession.objects.all()
    if request.method == "POST":
        course_name=request.POST.get('course_name')
        if AddCourse.objects.filter(course_name=course_name).exists():
            messages.error(request, "This Course already exists!")
        else:
            AddCourse.objects.create(
                course_name=course_name,
                academic_session=request.POST.get('academic_session'),
                course_code=request.POST.get('course_code'),
                level=request.POST.get('level'),
                duration=request.POST.get('duration'),
                status=request.POST.get('status'),
                description=request.POST.get('description'),
                Dor=datetime.now()
            )
            messages.success(request,"Course added successfully.")
    return render(request, 'superadmin/add_course.html',{'session_data':session_data})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def view_course(request):
    ab=AddCourse.objects.all()
    return render(request, 'superadmin/view_course.html',{'ab':ab})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def edit_course(request,id):
    s=AddCourse.objects.get(id=id)
    if request.method == "POST":
        s.academic_session=request.POST.get('academic_session')
        s.course_code=request.POST.get('course_code')
        s.course_name=request.POST.get('course_name')
        s.level=request.POST.get('level')
        s.duration=request.POST.get('duration')
        s.status=request.POST.get('status')
        s.description=request.POST.get('description')
        s.save()
        messages.success(request,'Course updated successfully')
        return redirect('view_course')
    return render(request,'superadmin/edit_course.html',{'s':s})


@login_required
def delete_course(request,id):
    s=AddCourse.objects.get(id=id)
    s.delete()
    messages.success(request,'Course deleted successfully')
    return redirect('view_course')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def add_subject(request):
    teacher_data=AddTeacher.objects.all()
    course_data=AddCourse.objects.all()
    if request.method == "POST":
        AddSubject.objects.create(
            course=request.POST.get('course'),
            subject_code=request.POST.get('subject_code'),
            subject_name=request.POST.get('subject_name'),
            semester=request.POST.get('semester'),
            credits=request.POST.get('credits'),
            teacher=request.POST.get('teacher'),
            status=request.POST.get('status'),
            description=request.POST.get('description'),
            Dor=datetime.now()
        )
        messages.success(request,"Subject created Successfully")
    return render(request, 'superadmin/add_subject.html',{'course_data':course_data,'teacher_data':teacher_data})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def view_subject(request):
    ab=AddSubject.objects.all()
    return render(request, 'superadmin/view_subject.html',{'ab':ab})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def edit_subject(request,id):
    s=AddSubject.objects.get(id=id)
    if request.method == "POST":
        s.course=request.POST.get('course')
        s.subject_code=request.POST.get('subject_code')
        s.subject_name=request.POST.get('subject_name')
        s.semester=request.POST.get('semester')
        s.credits=request.POST.get('credits')
        s.teacher=request.POST.get('teacher')
        s.status=request.POST.get('status')
        s.description=request.POST.get('description')
        s.save()
        messages.success(request,'Subject updated successfully')
        return redirect('view_subject')
    return render(request,'superadmin/edit_subject.html',{'s':s})


@login_required
def delete_subject(request,id):
    s=AddSubject.objects.get(id=id)
    s.delete()
    messages.success(request,'Subject deleted successfully')
    return redirect('view_subject')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def add_teacher(request):
    if request.method == "POST":
        employee_id=request.POST.get('employee_id')
        teacher_name=request.POST.get('teacher_name')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        department=request.POST.get('department')
        designation=request.POST.get('designation')
        username=request.POST.get('username')
        password=request.POST.get('password')
        status=request.POST.get('status')

        user=User.objects.create_user(
        username=username,
        password=password,
        email=email
        )
        AddTeacher.objects.create(
            user=user,
            employee_id=employee_id,
            teacher_name=teacher_name,
            email=email,
            mobile=mobile,
            department=department,
            designation=designation,
            username=username,
            password=password,
            status=status,
        )
        messages.success(request,'Teacher added successfully')
        return redirect('add_teacher')
    return render(request, 'superadmin/add_teacher.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def add_bulkteacher(request):
    if request.method == "POST":
        file=request.FILES.get('csv_file')
        data=file.read().decode('utf-8-sig').splitlines()
        header=csv.DictReader(data)
        header.fieldnames=[
            field.strip().lower()
            for field in header.fieldnames
        ]
        for row in header:
            #pprint(row['enrollment_no])
            user=User.objects.create_user(
                username=row['username'],
                password=row['password'],
                email=row['email']
            )
            AddTeacher.objects.create(
                user=user,
                employee_id=row['employee_id'],
                teacher_name=row['teacher_name'],
                email=row['email'],
                mobile=row['mobile'],
                department=row['department'],
                designation=row['designation'],
                username=row['username'],
                password=row['password'],
                status=row['status']
            )
            messages.success(request,'Teachers added successfully')
    return render(request,'superadmin/add_bulkteacher.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def view_teacher(request):
    ab=AddTeacher.objects.all()
    return render(request, 'superadmin/view_teacher.html',{'ab':ab})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def edit_teacher(request,id):
    s=AddTeacher.objects.get(id=id)
    if request.method == "POST":
        s.employee_id=request.POST.get('employee_id')
        s.teacher_name=request.POST.get('teacher_name')
        s.email=request.POST.get('email')
        s.mobile=request.POST.get('mobile')
        s.department=request.POST.get('department')
        s.designation=request.POST.get('designation')
        s.username=request.POST.get('username')
        s.password=request.POST.get('password')
        s.status=request.POST.get('status')
        s.save()
        messages.success(request,'Teacher updated successfully')
        return redirect('view_teacher')
    return render(request,'superadmin/edit_teacher.html',{'s':s})


@login_required
def delete_teacher(request,id):
    s=AddTeacher.objects.get(id=id)
    s.delete()
    messages.success(request,'Teacher deleted successfully')
    return redirect('view_teacher')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def add_bulkstudent(request):

    if request.method == "POST":
        file=request.FILES.get('csv_file')
        data=file.read().decode('utf-8').splitlines()
        header=csv.DictReader(data)
        for row in header:
            #pprint(row['enrollment_no])
            user=User.objects.create_user(
                username=row['username'],
                password=row['password'],
                email=row['email']
            )
            AddStudent.objects.create(
                user=user,
                enrollment_no=row['enrollment_no'],
                student_name=row['student_name'],
                email=row['email'],
                mobile=row['mobile'],
                course=row['course'],
                session=row['session'],
                semester=row['semester'],
                username=row['username'],
                password=row['password'],
                status=row['status']
            )
            messages.success(request,'Student created successfully')
    return render(request, 'superadmin/add_bulkstudent.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def add_student(request):
    session_data=AddSession.objects.all()
    course_data=AddCourse.objects.all()
    if request.method == "POST":
        enrollment_no=request.POST.get('enrollment_no')
        student_name=request.POST.get('student_name')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        session=request.POST.get('session')
        course=request.POST.get('course')
        semester=request.POST.get('semester')
        username=request.POST.get('username')
        password=request.POST.get('password')
        status=request.POST.get('status')
        
        user=User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            email=request.POST.get('email'),
        )
        AddStudent.objects.create(
            user=user,
            enrollment_no=enrollment_no,
            student_name=student_name,
            email=email,
            mobile=mobile,
            session=session,
            course=course,
            semester=semester,
            username=username,
            password=password,
            status=status
        )
        messages.success(request,"Students Added Successfully")
        return redirect(add_student)
    return render(request,'superadmin/add_student.html',{'session_data':session_data,'course_data':course_data})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def view_student(request):
    ab=AddStudent.objects.all()
    return render(request, 'superadmin/view_student.html',{'ab':ab})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def edit_student(request,enrollment_no):
    s=AddStudent.objects.get(enrollment_no=enrollment_no)
    if request.method == "POST":
        s.enrollment_no=request.POST.get('enrollment_no')
        s.student_name=request.POST.get('student_name')
        s.email=request.POST.get('email')
        s.mobile=request.POST.get('mobile')
        s.session=request.POST.get('session')
        s.course=request.POST.get('course')
        s.semester=request.POST.get('semester')
        s.username=request.POST.get('username')
        s.password=request.POST.get('password')
        s.status=request.POST.get('status')
        s.save()
        messages.success(request,'Student updated successfully')
        return redirect('view_student')
    return render(request,'superadmin/edit_student.html',{'s':s})

@login_required
def delete_student(request,enrollment_no):
    s=AddStudent.objects.get(enrollment_no=enrollment_no)
    s.delete()
    messages.success(request,'Student deleted successfully')
    return redirect(view_student)


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def upload_study_material(request):
    course_data=AddCourse.objects.all()
    subject_data=AddSubject.objects.all()
    if request.method == "POST":
        UploadSM.objects.create(
            title=request.POST.get('title'),
            material_type=request.POST.get('material_type'),
            course=request.POST.get('course'),
            subject=request.POST.get('subject'),
            material_file=request.FILES.get('material_file'),
            external_url=request.POST.get('external_url'),
            status=request.POST.get('status'),
            description=request.POST.get('description'),
            create_by=request.user
        )
        messages.success(request,"Upload Successfully")
        return redirect(upload_study_material)

    return render(request,'superadmin/upload_study_material.html',{'course_data':course_data,'subject_data':subject_data})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def view_study_material(request):
    ab=UploadSM.objects.all()
    return render(request, 'superadmin/view_study_material.html',{'ab':ab})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def edit_study_material(request,id):
    s=UploadSM.objects.get(id=id)
    if request.method == "POST":
        s.title=request.POST.get('title')
        s.material_type=request.POST.get('material_type')
        s.course=request.POST.get('course')
        s.subject=request.POST.get('subject')
        s.material_file=request.FILES.get('material_file')
        s.external_url=request.POST.get('external_url')
        s.status=request.POST.get('status')
        s.description=request.POST.get('description')
        s.create_by=request.user 
        s.save()
        messages.success(request,'SM updated successfully')
        return redirect(view_study_material)
    return render(request,'superadmin/edit_study_material.html',{'s':s})  

@login_required
def delete_study_material(request,id):
    ab=UploadSM.objects.get(id=id)
    ab.delete()
    messages.success(request,'SM deleted successfully')
    return redirect(view_study_material)  


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def add_task(request):
    course_data=AddCourse.objects.all()
    subject_data=AddSubject.objects.all()
    if request.method == "POST":
        AddTask.objects.create(
            title=request.POST.get('title'),
            due_date=request.POST.get('due_date'),
            course=request.POST.get('course'),
            subject=request.POST.get('subject'),
            total_marks=request.POST.get('total_marks'),
            attachment=request.POST.get('attachment'),
            status=request.POST.get('status'),
            instruction=request.POST.get('instruction'),
            Dor_date=datetime.now(),
            create_by=request.user
        )
        messages.success(request,"Task Added Successfully")
        return redirect(add_task)
    return render(request, 'superadmin/add_task.html',{'course_data':course_data,'subject_data':subject_data})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def view_task(request):
    ab=AddTask.objects.all()
    return render(request, 'superadmin/view_task.html',{'ab':ab})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def edit_task(request,id):
    course_data=AddCourse.objects.all()
    subject_data=AddSubject.objects.all()
    ab=AddTask.objects.get(id=id)
    if request.method == "POST":
        ab.title=request.POST.get('title')
        ab.due_date=request.POST.get('due_date')
        ab.course=request.POST.get('course')
        ab.subject=request.POST.get('subject')
        ab.total_marks=request.POST.get('total_marks')
        ab.attachment=request.FILES.get('attachment')
        ab.status=request.POST.get('status')
        ab.instruction=request.POST.get('instruction')
        ab.Dor_date=datetime.now()
        ab.create_by=request.user
        ab.save()
        messages.success(request,'Task updated successfully')
        return redirect(view_task)
    return render(request,'superadmin/edit_task.html',{'ab':ab,'course_data':course_data,'subject_data':subject_data})

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def delete_task(request,id):
    ab=AddTask.objects.get(id=id)
    ab.delete()
    messages.success(request,'Task deleted successfully')
    return redirect(view_task)


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def add_test(request):
    course_data=AddCourse.objects.all()
    subject_data=AddSubject.objects.all()
    if request.method == "POST":
        Test.objects.create(
            test_title=request.POST.get('test_title'),
            test_date=request.POST.get('test_date'),
            course=request.POST.get('course'),
            subject=request.POST.get('subject'),
            start_time=request.POST.get('start_time'),
            duration=request.POST.get('duration'),
            total_marks=request.POST.get('total_marks'),
            status=request.POST.get('status'),
        )
        messages.success(request,'Test added successfully')
    return render(request, 'superadmin/add_test.html',{'course_data':course_data,'subject_data':subject_data})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def view_test(request):
    ab=Test.objects.all()
    return render(request, 'superadmin/view_test.html',{"ab":ab})


@login_required
def question_bank(request,id):
    data=Test.objects.get(id=id)
    qc=Question_bank.objects.filter(test=data)
    if request.method == "POST":
        Question_bank.objects.create(
            test=data,
            question=request.POST.get('question'),
            option_a=request.POST.get('option_a'),
            option_b=request.POST.get('option_b'),
            option_c=request.POST.get('option_c'),
            option_d=request.POST.get('option_d'),
            correct_option=request.POST.get('correct_option'),
            marks=request.POST.get('marks'),
        )
        messages.success(request,'Question updated successfully')
    return render(request,'superadmin/single_question.html',{'data':data,'qc':qc})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def bulk_question(request,id):
    tdata=Test.objects.get(id=id)
    qc=Question_bank.objects.filter(test=tdata)
    file=request.FILES.get('csv_file')
    if file:
        data=file.read().decode('utf-8').splitlines()
        header=csv.DictReader(data)
        for row in header:
            Question_bank.objects.create(
                test=tdata,
                question=row['question'],
                option_a=row['option_a'],
                option_b=row['option_b'],
                option_c=row['option_c'],
                option_d=row['option_d'],
                correct_option=row['correct_option'],
                marks=row['marks'],
            )
            messages.success(request,'Questions added successfully')
            return redirect('view_test')
    return render(request,'superadmin/bulk_question.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def edit_test(request,id):
    s=Test.objects.get(id=id)
    if request.method == "POST":
        s.test_title=request.POST.get('test_title')
        s.test_date=request.POST.get('test_date')
        s.course=request.POST.get('course')
        s.subject=request.POST.get('subject')
        s.start_time=request.POST.get('start_time')
        s.duration=request.POST.get('duration')
        s.total_marks=request.POST.get('total_marks')
        s.status=request.POST.get('status')
        s.save()
        messages.success(request,'Test updated successfully')
        return redirect('view_test')
    return render(request,'superadmin/edit_test.html',{'s':s})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def delete_test(request,id):
    ab=Test.objects.get(id=id)
    ab.delete()
    messages.success(request,'Test deleted successfully')
    return redirect('view_test')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def test_result(request):
    ab=TestResult.objects.all()
    return render(request, 'superadmin/test_result.html',{'ab':ab})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def student_attendance(request):
    course_data=AddCourse.objects.all()
    course=request.GET.get('course')
    data=[]
    messages.success(request,'')
    if course:
        data=AddStudent.objects.filter(course=course)
        if not data:
            print('No students found for this course')
            messages.success(request,'No students found for this course')
    return render(request, 'superadmin/student_attendance.html',{'course_data':course_data,'data':data,'course':course})


def save_method(request):
    if request.method == "POST":
        course=request.POST.get('course')
        data=AddStudent.objects.filter(course=course)

        for i in data:
            Attendance.objects.create(
                enrollment_no=i.enrollment_no,
                name=i.student_name,
                course=i.course,
                mobile=i.mobile,
                teacher_name=request.user.username,
                Date=datetime.now(),
                status=request.POST.get(f"status_{i.enrollment_no}","Absent")
            )
        messages.success(request,"Attendance saved Successfully")
    return redirect('student_attendance')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def attendance_report(request):

    ab = AddCourse.objects.all()

    course = request.GET.get('course', '')
    students = []

    if course:
        students = AddStudent.objects.filter(course=course)

        for i in students:

            i.total = Attendance.objects.filter(
                enrollment_no=i.enrollment_no
            ).count()

            i.present = Attendance.objects.filter(
                enrollment_no=i.enrollment_no,
                status="Present"
            ).count()

            i.absent = Attendance.objects.filter(
                enrollment_no=i.enrollment_no,
                status="Absent"
            ).count()

            if i.total > 0:
                i.percent = round(i.present * 100 / i.total, 1)
            else:
                i.percent = 0

    return render(
        request,
        'superadmin/attendance_report.html',
        {
            'ab': ab,
            'course': course,
            'students': students,
        }
    )


# @cache_control(no_cache=True,must_revalidate=True,no_store=True)
# @login_required
# def view_class(request):
#     return render(request, 'superadmin/view_class.html')

def delete_class(request,id):
    ab=get_object_or_404(GoogleMeeting,id=id)
    if not (request.user.is_superuser or ab.teacher_id == request.user.id):
        return HttpResponse('You can delete only your own class.', status=403)
    ab.delete()
    return redirect('superadmin_classes' if request.user.is_superuser else 't_view_class')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def announcements(request):
    if request.method == "POST":
        Announcements.objects.create(
        title=request.POST.get('title'),
        audience=request.POST.get('audience'),
        priority=request.POST.get('priority'),
        publish_date=request.POST.get('publish_date'),
        expiry_date=request.POST.get('expiry_date'),
        message=request.POST.get('message'),
        )
        messages.success(request,'Added successfully')
    return render(request, 'superadmin/announcements.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def notification(request):
    if request.method == "POST":
        Notifications.objects.create(
        title=request.POST.get('title'),
        audience=request.POST.get('audience'),
        module=request.POST.get('modeule'),
        message=request.POST.get('message'),
        )
        messages.success(request,'Added successfully')
    return render(request, 'superadmin/notification.html')






'''///////////////////////////////// Teacher Zone ///////////////////////////////////////'''


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def teacherdash(request):

    # Logged-in teacher
    teacher = AddTeacher.objects.get(user=request.user)

    # -------------------------------
    # TEACHER KE SUBJECTS
    # -------------------------------

    teacher_subjects = AddSubject.objects.filter(
        teacher=teacher.teacher_name
    )

    # My Subjects
    current_subject = teacher_subjects.count()

    # -------------------------------
    # TEACHER KE COURSES
    # -------------------------------

    teacher_courses = list(
        teacher_subjects
        .exclude(course__isnull=True)
        .exclude(course="")
        .values_list("course", flat=True)
        .distinct()
    )

    # My Courses
    current_course = len(teacher_courses)

    # -------------------------------
    # ASSIGNMENTS
    # -------------------------------

    current_assignment = AddTask.objects.filter(
        create_by=request.user
    ).count()

    # -------------------------------
    # ONLINE CLASSES
    # -------------------------------

    current_online_class = GoogleMeeting.objects.filter(
        teacher=request.user
    ).count()

    # -------------------------------
    # SUBMISSIONS TO REVIEW
    # -------------------------------

    current_submission = TaskSubmission.objects.filter(
        task__create_by=request.user
    ).count()

    # -------------------------------
    # STUDENTS IN MY COURSES
    # -------------------------------

    current_students = AddStudent.objects.filter(
        course__in=teacher_courses
    ).count()

    # -------------------------------
    # STUDY MATERIALS
    # -------------------------------

    current_material = UploadSM.objects.filter(
        create_by=request.user
    ).count()

    # -------------------------------
    # ONLINE TESTS
    # -------------------------------

    current_test = Test.objects.filter(
        course__in=teacher_courses
    ).count()

    context = {
        "current_course": current_course,
        "current_subject": current_subject,
        "current_assignment": current_assignment,
        "current_online_class": current_online_class,
        "current_submission": current_submission,
        "current_students": current_students,
        "current_material": current_material,
        "current_test": current_test,
    }

    return render(
        request,
        "teacher/teacherdashboard.html",
        context
    )


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_current_session(request):
    data=AddSession.objects.all()
    return render(request,'teacher/current_session.html',{'data':data})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_my_courses(request):
    teacher = AddTeacher.objects.get(user=request.user)
    subjects = AddSubject.objects.filter(teacher=teacher.teacher_name)
    courses = AddCourse.objects.filter(course_name__in=subjects.values_list('course', flat=True))
    return render(request, 'teacher/mycourses.html', {'teacher': teacher,'courses': courses,'subjects': subjects,})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_my_subjects(request):
    teacher = AddTeacher.objects.get(user=request.user)
    subjects = AddSubject.objects.filter(teacher=teacher.teacher_name)
    courses = AddCourse.objects.filter(course_name__in=subjects.values_list('course', flat=True))
    return render(request,'teacher/mysubjects.html', {'teacher': teacher,'courses': courses,'subjects': subjects,})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_upload_sm(request):
    course_data=AddCourse.objects.all()
    subject_data=AddSubject.objects.all()
    if request.method == "POST":
        UploadSM.objects.create(
            title=request.POST.get('title'),
            material_type=request.POST.get('material_type'),
            course=request.POST.get('course'),
            subject=request.POST.get('subject'),
            material_file=request.FILES.get('material_file'),
            external_url=request.POST.get('external_url'),
            status=request.POST.get('status'),
            description=request.POST.get('description'),
            create_by=request.user
        )
        messages.success(request,"SM Upload Successfully")
        return redirect(t_upload_sm)
    return render(request,'teacher/upload_sm.html',{'course_data':course_data,'subject_data':subject_data})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_view_sm(request):
    ab=UploadSM.objects.all()
    return render(request,'teacher/view_sm.html',{'ab':ab})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_edit_sm(request,id):
    s=UploadSM.objects.get(id=id)
    if request.method == "POST":
        s.title=request.POST.get('title')
        s.material_type=request.POST.get('material_type')
        s.course=request.POST.get('course')
        s.subject=request.POST.get('subject')
        s.material_file=request.FILES.get('material_file')
        s.external_url=request.POST.get('external_url')
        s.status=request.POST.get('status')
        s.description=request.POST.get('description')
        s.create_by=request.user 
        s.save()
        messages.success(request,'SM updated successfully')
        return redirect(t_view_sm)
    return render(request,'teacher/edit_sm.html',{'s':s})  

@login_required
def t_delete_sm(request,id):
    ab=UploadSM.objects.get(id=id)
    ab.delete()
    messages.success(request,'SM deleted successfully')
    return redirect(t_view_sm) 


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_add_task(request):
    course_data=AddCourse.objects.all()
    subject_data=AddSubject.objects.all()
    if request.method == "POST":
        AddTask.objects.create(
            title=request.POST.get('title'),
            due_date=request.POST.get('due_date'),
            course=request.POST.get('course'),
            subject=request.POST.get('subject'),
            total_marks=request.POST.get('total_marks'),
            attachment=request.FILES.get('attachment'),
            status=request.POST.get('status'),
            instruction=request.POST.get('instruction'),
            Dor_date=datetime.now(),
            create_by=request.user
        )
        messages.success(request,"Task Added Successfully")
        return redirect(t_add_task)
    return render(request,'teacher/add_task.html',{'course_data':course_data,'subject_data':subject_data})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_view_task(request):
    ab=AddTask.objects.all()
    return render(request,'teacher/view_task.html',{'ab':ab})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_edit_task(request,id):
    course_data=AddCourse.objects.all()
    subject_data=AddSubject.objects.all()
    ab=AddTask.objects.get(id=id)
    if request.method == "POST":
        ab.title=request.POST.get('title')
        ab.due_date=request.POST.get('due_date')
        ab.course=request.POST.get('course')
        ab.subject=request.POST.get('subject')
        ab.total_marks=request.POST.get('total_marks')
        ab.attachment=request.FILES.get('attachment')
        ab.status=request.POST.get('status')
        ab.instruction=request.POST.get('instruction')
        ab.Dor_date=datetime.now()
        ab.create_by=request.user
        ab.save()
        messages.success(request,'Task updated successfully')
        return redirect(t_view_task)
    return render(request,'teacher/edit_task.html',{'ab':ab,'course_data':course_data,'subject_data':subject_data})

@login_required
def t_delete_task(request,id):
    ab=AddTask.objects.get(id=id)
    ab.delete()
    messages.success(request,'Task deleted successfully')
    return redirect(t_view_task)



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_submission(request):
    ab=TaskSubmission.objects.all()
    return render(request,'teacher/submission.html',{'ab':ab})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_add_test(request):
    course_data=AddCourse.objects.all()
    subject_data=AddSubject.objects.all()
    if request.method == "POST":
        Test.objects.create(
            test_title=request.POST.get('test_title'),
            test_date=request.POST.get('test_date'),
            course=request.POST.get('course'),
            subject=request.POST.get('subject'),
            start_time=request.POST.get('start_time'),
            duration=request.POST.get('duration'),
            total_marks=request.POST.get('total_marks'),
            status=request.POST.get('status'),
        )
        messages.success(request,'Test Added successfully')
    return render(request,'teacher/add_test.html',{'course_data':course_data,'subject_data':subject_data})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_view_test(request):
    ab=Test.objects.all()
    return render(request,'teacher/view_test.html',{'ab':ab})


@login_required
def t_question_bank(request,id):
    data=Test.objects.get(id=id)
    qc=Question_bank.objects.filter(test=data)
    if request.method == "POST":
        Question_bank.objects.create(
            test=data,
            question=request.POST.get('question'),
            option_a=request.POST.get('option_a'),
            option_b=request.POST.get('option_b'),
            option_c=request.POST.get('option_c'),
            option_d=request.POST.get('option_d'),
            correct_option=request.POST.get('correct_option'),
            marks=request.POST.get('marks'),
        )
        messages.success(request,'Question Added Successfully')
    return render(request,'teacher/single_question.html',{'data':data,'qc':qc})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_bulk_question(request,id):
    tdata=Test.objects.get(id=id)
    qc=Question_bank.objects.filter(test=tdata)
    file=request.FILES.get('csv_file')
    if file:
        data=file.read().decode('utf-8').splitlines()
        header=csv.DictReader(data)
        for row in header:
            Question_bank.objects.create(
                test=tdata,
                question=row['question'],
                option_a=row['option_a'],
                option_b=row['option_b'],
                option_c=row['option_c'],
                option_d=row['option_d'],
                correct_option=row['correct_option'],
                marks=row['marks'],
            )
            messages.success(request,'Questions Added Successfully')
        return redirect('t_view_test')
    return render(request,'teacher/bulk_question.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_edit_test(request,id):
    s=Test.objects.get(id=id)
    if request.method == "POST":
        s.test_title=request.POST.get('test_title')
        s.test_date=request.POST.get('test_date')
        s.course=request.POST.get('course')
        s.subject=request.POST.get('subject')
        s.start_time=request.POST.get('start_time')
        s.duration=request.POST.get('duration')
        s.total_marks=request.POST.get('total_marks')
        s.status=request.POST.get('status')
        s.save()
        messages.success(request,'Test updated successfully')
        return redirect('t_view_test')
    return render(request,'teacher/edit_test.html',{'s':s})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_delete_test(request,id):
    ab=Test.objects.get(id=id)
    ab.delete()
    messages.success(request,'Test deleted successfully')
    return redirect('t_view_test')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_result(request):
    ab=TestResult.objects.all()
    return render(request,'teacher/result.html',{"ab":ab})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_mark_attendance(request):
    course_data=AddCourse.objects.all()
    course=request.GET.get('course')
    data=[]
    messages.success(request,'')
    if course:
        data=AddStudent.objects.filter(course=course)
        if not data:
            print('No students found for this course')
            messages.success(request,'No students found for this course')
    return render(request,'teacher/attendance.html',{'course_data':course_data,'data':data,'course':course})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_save_method(request):
    if request.method == "POST":
        course=request.POST.get('course')
        data=AddStudent.objects.filter(course=course)

        for i in data:
            Attendance.objects.create(
                enrollment_no=i.enrollment_no,
                name=i.student_name,
                course=i.course,
                mobile=i.mobile,
                teacher_name=request.user.username,
                Date=datetime.now(),
                status=request.POST.get(f"status_{i.enrollment_no}","Absent")
            )
        messages.success(request,"Attendance saved Successfully")
    return redirect('t_mark_attendance')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_report(request):
    ab = AddCourse.objects.all()
    
    course = request.GET.get('course', '')
    students = []
    
    if course:
        students = AddStudent.objects.filter(course=course)
    
        for i in students:
    
                i.total = Attendance.objects.filter(
                    enrollment_no=i.enrollment_no
                ).count()
    
                i.present = Attendance.objects.filter(
                    enrollment_no=i.enrollment_no,
                    status="Present"
                ).count()
    
                i.absent = Attendance.objects.filter(
                    enrollment_no=i.enrollment_no,
                    status="Absent"
                ).count()
    
                if i.total > 0:
                    i.percent = round(i.present * 100 / i.total, 1)
                else:
                    i.percent = 0
    return render(request,'teacher/report.html',{'ab': ab,'course': course,'students': students})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_add_class(request):
    if not hasattr(request.user, 'Teacher'):
        return HttpResponse('Only teachers can schedule classes.', status=403)
    teacher = request.user.Teacher
    # Teacher sirf apne assigned subjects/courses ki class schedule kar sakta hai
    subjects = AddSubject.objects.filter(teacher=teacher.teacher_name)
    courses = AddCourse.objects.filter(course_name__in=subjects.values_list('course', flat=True))
    return render(request,'teacher/add_class.html',{
        'courses': courses,
        'subjects': subjects,
        'google_connected': GoogleCredential.objects.filter(connected=True).exists(),
    })


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_view_class(request):
    if not hasattr(request.user, 'Teacher'):
        return HttpResponse('Only teachers can view this page.', status=403)
    meetings = GoogleMeeting.objects.filter(teacher=request.user).order_by('-class_date','-class_time')
    return render(request,'teacher/view_class.html',{'meetings': refreshmeeting_statuses(meetings)})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_announcements(request):
    data=Announcements.objects.filter(audience__in=["all","teacher"]).order_by("-publish_date")
    return render(request,'teacher/announcement.html',{'data':data})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_notifications(request):
    data=Notifications.objects.filter(audience__in=["all","teacher"])
    return render(request,'teacher/notification.html',{'data':data})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def t_profile(request):
    return render(request,'teacher/profile.html')



'''///////////////////////////////// Student Zone ///////////////////////////////////////'''

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def studentdash(request):
    student=AddStudent.objects.get(user=request.user)
    #current subjects
    subjects=AddStudent.objects.filter(course=student.course)
    current_subject=subjects.count()
    assignments=AddTask.objects.filter(course=student.course)
    current_assignment=assignments.count()
    onlineclass=GoogleMeeting.objects.filter(course=student.course)
    current_class=onlineclass.count()
    attendance=Attendance.objects.filter(enrollment_no=student.enrollment_no)
    current_attendance=attendance.count()
    present=attendance.filter(status="Present").count()
    attendance_percentage=(round((present/current_attendance)*100)if current_attendance > 0 else 0 )
    test=Test.objects.filter(course=student.course)
    current_test=test.count()
    SM=UploadSM.objects.filter(course=student.course)
    current_SM=SM.count()
    submit=TaskSubmission.objects.filter(submit_to=student.username)
    current_Submission=submit.count()
    return render(request,'student/studentdash.html',{"current_subject":current_subject,"current_assignment":current_assignment,"current_class":current_class,"attendance_percentage":attendance_percentage,"current_test":current_test,"current_SM":current_SM,"current_Submission":current_Submission})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def s_current_session(request):
    data=AddSession.objects.all()
    return render(request,'student/current_session.html',{"data":data})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def s_course_detail(request):
    student=AddStudent.objects.get(user=request.user)
    course=AddCourse.objects.filter(course_name=student.course).first()
    return render(request,'student/course_details.html',{'student':student,'course':course})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def s_my_subjects(request):
    student=AddStudent.objects.get(user=request.user)
    course=AddCourse.objects.filter(course_name=student.course).first()
    subject=AddSubject.objects.filter(course=student.course)
    return render(request,'student/my_subjects.html',{'student':student,'course':course,'subject':subject})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def s_study_material(request):
    material_type=request.POST.get('get_value')
    user=AddStudent.objects.get(user=request.user)
    btn_show=UploadSM.objects.all()
    if material_type:
        data=UploadSM.objects.filter(course=user.course,material_type=material_type)
    else:
        data=UploadSM.objects.filter(course=user.course) 
    return render(request,'student/study_material.html',{'data':data,'btn_show':btn_show})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def s_assignments(request):
    ab=AddTask.objects.all()
    return render(request,'student/assignments.html',{'ab':ab})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def task_submit(request,id):
    data=AddTask.objects.get(id=id)
    if request.method == "POST":
        file=request.FILES.get('file')
        TaskSubmission.objects.create(
            task=data,
            submitted_file=file,
            submit_to=request.user,
            status="submitted"
        )
        messages.success(request,'Task Submitted Successfully')
        return redirect('s_submission')
    return render(request,'student/task_submit.html',{'data':data})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def s_submission(request):
    ab=TaskSubmission.objects.all()
    return render(request,'student/submission.html',{'ab':ab})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def s_programming_lab(request):
    return render(request,'student/programming_lab.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def s_online_test(request):
    show=Test.objects.all()
    for test in show:
        test.question_count = Question_bank.objects.filter(test=test).count()
    return render(request,'student/online_test.html',{'show':show})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def test_dt(request,id):
    test=Test.objects.get(id=id)
    question=Question_bank.objects.filter(test=test)
    return render(request,'student/start_test.html',{'question':question,'test':test})



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def start_test(request, id):

    test = Test.objects.get(id=id)

    # Check already submitted
    result = TestResult.objects.filter(
        student=request.user,
        test=test
    ).first()

    if result:
        return render(
            request,
            'student/test_result.html',
            {
                'test': test,
                'result': result,
                'already_submitted': True
            }
        )

    questions = Question_bank.objects.filter(test=test)

    if request.method == "POST":

        marks = 0

        for q in questions:

            # HTML mein name="q{{ q.id }}" hai
            answer = request.POST.get("q" + str(q.id))

            if answer == q.correct_option:
                marks += q.marks

        # Result ek hi baar save hoga
        result = TestResult.objects.create(
            student=request.user,
            test=test,
            obtained_marks=marks
        )

        return render(
            request,
            'student/test_result.html',
            {
                'test': test,
                'result': result,
                'already_submitted': False
            }
        )

    return render(
        request,
        'student/start_test.html',
        {
            'test': test,
            'question': questions
        }
    )


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def s_my_results(request):
    ab=TestResult.objects.filter(student=request.user)
    return render(request,'student/result.html',{'ab':ab})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def s_attendance(request):

    # Logged-in student ka record
    student = AddStudent.objects.get(user=request.user)

    # Sirf isi student ki attendance
    attendance = Attendance.objects.filter(
        enrollment_no=student.enrollment_no
    ).order_by('-Date')

    # Attendance calculation
    total = attendance.count()

    present = attendance.filter(
        status="Present"
    ).count()

    absent = attendance.filter(
        status="Absent"
    ).count()

    if total > 0:
        percentage = round((present * 100) / total, 1)
    else:
        percentage = 0

    return render(request, 'student/attendance.html', {
        'student': student,
        'attendance': attendance,
        'total': total,
        'present': present,
        'absent': absent,
        'percentage': percentage,
    })


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def s_class_schedule(request):
    return render(request,'student/online_class.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def s_announcements(request):
    data=Announcements.objects.filter(audience__in=["all","student"]).order_by("-publish_date")
    return render(request,'student/announcement.html',{"data":data})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def s_notifications(request):
    data=Notifications.objects.filter(audience__in=["all","student"])
    return render(request,'student/notification.html',{"data":data})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def s_profile(request):
    return render(request,'student/profile.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def s_help(request):
    return render(request,'student/help.html')




'''//////////////////////////////////// Logout ///////////////////////////////////////'''

def logout_view(request):
    logout(request)
    return redirect(Home)




'''//////////////////////////////////// Schedule Class /////////////////////////////////////'''

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add_class(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.user.is_superuser:
        return redirect('superadmin_schedule_class')
    if hasattr(request.user, 'Teacher'):
        return redirect('teacher_schedule_class')
    return HttpResponse('Only teachers and superadmin can schedule classes.', status=403)



def superadmin_schedule_class(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if not request.user.is_superuser:
        return HttpResponse('Only superadmin can schedule classes.', status=403)
    return render(request, 'superadmin/add_class.html', {
        'teachers': AddTeacher.objects.select_related('user').order_by("teacher_name"),
        'courses': AddCourse.objects.all(),
        'subjects': AddSubject.objects.all(),
        'fixed_teacher': None,
    })


def teacher_schedule_class(request):

    if not request.user.is_authenticated:
        return redirect('home')

    if not AddTeacher.objects.filter(user=request.user).exists():
        return HttpResponse('Only teachers can schedule classes.', status=403)

    return redirect('t_add_class')


def refreshmeeting_statuses(queryset):
    from datetime import datetime, timedelta
    from django.utils import timezone
    now = timezone.now()
    for item in queryset.filter(status='live'):
        start = item.created_at
        if not start:
            start = datetime.combine(item.class_date, item.class_time)
            if timezone.is_naive(start):
                start = timezone.make_aware(start, timezone.get_current_timezone())
        if now >= start + timedelta(minutes=item.duration):
            item.status = 'closed'
            item.save(update_fields=['status'])
    return queryset







'''//////////////////////////////////// Progamming Lab /////////////////////////////////'''

@cache_control(
    no_cache=True,
    must_revalidate=True,
    no_store=True
)
def student_code_lab(request):
    context = {
        'languages': LANGUAGES,
        'starter_code': STARTER_CODE,
    }

    return render(
        request,
        'student/code_lab.html',
        context
    )


def run_student_code(request):

    language = (request.POST.get('language') or '').strip()
    source_code = request.POST.get('source_code') or ''
    stdin = request.POST.get('stdin') or ''

    if len(source_code) > 50000:
        return JsonResponse({
            'ok': False,
            'error': 'Maximum code size is 50,000 characters.'
        }, status=400)

    if len(stdin) > 10000:
        return JsonResponse({
            'ok': False,
            'error': 'Maximum input size is 10,000 characters.'
        }, status=400)

    result, error = run_code(
        language,
        source_code,
        stdin
    )

    if error:
        return JsonResponse({
            'ok': False,
            'error': error
        }, status=502)

    return JsonResponse({
        'ok': True,
        **result
    })