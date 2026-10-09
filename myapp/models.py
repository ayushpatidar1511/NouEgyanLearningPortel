from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AddSession(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True)
    session_name=models.CharField(max_length=50,blank=None,null=True)
    status=models.CharField(max_length=20,blank=None,null=True)
    start_date=models.DateField()
    end_date=models.DateField()
    Dor=models.DateTimeField(null=True)
    Dou=models.DateTimeField(null=True)
    Dod=models.DateTimeField(null=True)

    def __str__(self):
        return self.session_name

class AddCourse(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True)
    academic_session=models.CharField(max_length=20,blank=None,null=True)
    course_code=models.CharField(max_length=20,blank=None,null=True)
    course_name=models.CharField(max_length=50,blank=None,null=True)
    level=models.CharField(max_length=50,blank=None,null=True)
    duration=models.CharField(max_length=10,blank=None,null=True)
    status=models.CharField(max_length=10,blank=None,null=True)
    description=models.CharField(max_length=100,blank=None,null=True)
    Dor=models.DateTimeField(null=True)
    Dou=models.DateTimeField(null=True)
    Dod=models.DateTimeField(null=True)

    def __str__(self):
        return self.course_name


class AddSubject(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True)
    course=models.CharField(max_length=50,blank=None,null=True)
    subject_code=models.CharField(max_length=50,blank=None,null=True)
    subject_name=models.CharField(max_length=50,blank=None,null=True)
    semester=models.CharField(max_length=20,blank=None,null=True)
    credits=models.IntegerField(max_length=20,blank=None,null=True)
    teacher=models.CharField(max_length=50,blank=None,null=True)
    status=models.CharField(max_length=20,blank=None,null=True)
    description=models.CharField(max_length=100,blank=None,null=True)
    Dor=models.DateTimeField(null=True)
    Dou=models.DateTimeField(null=True)
    Dod=models.DateTimeField(null=True)

    def __str__(self):
        return self.subject_name


class AddTeacher(models.Model):
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="Teacher"
    )
    id=models.IntegerField(primary_key=True,auto_created=True)
    employee_id=models.CharField(max_length=20,blank=None,null=True)
    teacher_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50,blank=None,null=True)
    mobile=models.CharField(max_length=13,blank=None,null=True)
    department=models.CharField(max_length=50,blank=None,null=True)
    designation=models.CharField(max_length=50,blank=None,null=True)
    username=models.CharField(max_length=50,blank=None,null=True)
    password=models.CharField(max_length=50,blank=None,null=True)
    status=models.CharField(max_length=20,blank=None,null=True)
    Dor=models.DateTimeField(null=True)
    Dou=models.DateTimeField(null=True)
    Dod=models.DateTimeField(null=True)

    def __str__(self):
        return self.teacher_name


class AddStudent(models.Model):
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="Student"
    )
    enrollment_no=models.CharField(primary_key=True)
    student_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    mobile=models.CharField(max_length=50)
    session=models.CharField(max_length=20)
    course=models.CharField(max_length=50)
    semester=models.CharField(max_length=20)
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=16)
    status=models.CharField(max_length=20)

    def __str__(self):
        return self.student_name
    


class UploadSM(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True)
    title=models.CharField(max_length=50,unique=True)
    material_type=models.CharField(max_length=50)
    course=models.CharField(max_length=50)
    subject=models.CharField(max_length=50)
    material_file=models.FileField(upload_to='study_material/',null=True)
    external_url=models.CharField(max,null=True,blank=True)
    status=models.CharField(max_length=20)
    description=models.CharField(max_length=200,null=True,blank=True)
    create_by=models.ForeignKey(
        User,
        on_delete=models.SET_NULL,null=True
    )

    def __str__(self):
        return self.title

    
class AddTask(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True)
    title=models.CharField(max_length=50,unique=True)
    due_date=models.DateField()
    Dor_date=models.DateTimeField(null=True)
    course=models.CharField(max_length=50)
    subject=models.CharField(max_length=50)
    total_marks=models.IntegerField()
    attachment=models.FileField(upload_to='add_task',null=True)
    status=models.CharField(max_length=20)
    instruction=models.CharField(max_length=200)
    create_by=models.ForeignKey(
        User,
        on_delete=models.SET_NULL,null=True
    )
    
    def __str__(self):
        return self.title



class GoogleCredential(models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField(null=True,blank=True)
    connected = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Main Google Account"


class GoogleMeeting(models.Model):
    class_title = models.CharField(max_length=200)
    course = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    class_date = models.DateField()
    class_time = models.TimeField()
    duration = models.IntegerField()
    agenda = models.TextField(blank=True,null=True)
    meeting_url = models.URLField(blank=True,null=True)
    google_space_name = models.CharField(max_length=255,blank=True,null=True)
    status = models.CharField(max_length=20,default="scheduled")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.class_title



class Attendance(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True)
    enrollment_no=models.CharField(max_length=50)
    name=models.CharField(max_length=200)
    course=models.CharField(max_length=50)
    mobile=models.CharField(max_length=16)
    Date=models.DateTimeField(null=True)
    teacher_name=models.CharField(max_length=100)
    status=models.CharField(max_length=20)



class Announcements(models.Model):
    title=models.CharField(max_length=50)
    audience=models.CharField(max_length=20)
    priority=models.CharField(max_length=20)
    publish_date=models.DateTimeField()
    expiry_date=models.DateTimeField()
    message=models.CharField(max_length=200)


class Notifications(models.Model):
    title=models.CharField(max_length=50)
    audience=models.CharField(max_length=20)
    module=models.CharField(max_length=20)
    message=models.CharField(max_length=200)


class Test(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True)
    test_title=models.CharField(max_length=200)
    test_date=models.DateField()
    course=models.CharField(max_length=200)
    subject=models.CharField(max_length=200)
    start_time=models.TimeField()
    duration=models.IntegerField()
    total_marks=models.IntegerField()
    status=models.CharField(max_length=100)

    def __str__(self):
        return self.test_title


class Question_bank(models.Model):
    test=models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    question=models.CharField(max)
    option_a=models.CharField(max_length=200)
    option_b=models.CharField(max_length=200)
    option_c=models.CharField(max_length=200)
    option_d=models.CharField(max_length=200)
    correct_option=models.CharField(max_length=2)
    marks=models.IntegerField(max_length=2)



class TestResult(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    obtained_marks = models.PositiveIntegerField(default=0)
    

    class Meta:
        unique_together = ('student', 'test')




class TaskSubmission(models.Model):
    task=models.ForeignKey(
        AddTask,
        on_delete=models.CASCADE
    )
    submitted_file=models.FileField(upload_to='submission/')
    submit_to=models.CharField(max_length=50)
    status=models.CharField(max_length=50)