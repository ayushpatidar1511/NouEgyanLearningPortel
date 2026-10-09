from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Login url
    path('',views.Home,name='home'),

    # Superadmin urls
    path('superadmindash',views.superadmindash,name="superadmindash"),

    # superadmin - session urls
    path('superadmindash/add-session',views.add_session,name="add_session"),
    path('superadmindash/show-session',views.show_session,name="show_session"),
    path('superadmindash/edit-session/<int:id>',views.edit_session,name="edit_session"),
    path('superadmindash/delete-session/<int:id>',views.delete_session,name="delete_session"),

    # superadmin - course urls
    path('superadmindash/add-course',views.add_course,name="add_course"),
    path('superadmindash/view-course',views.view_course,name="view_course"),
    path('superadmindash/edit-course/<int:id>',views.edit_course,name="edit_course"),
    path('superadmindash/delete-course/<int:id>',views.delete_course,name="delete_course"),

    # superadmin - subject ulrs
    path('superadmindash/add-subject',views.add_subject,name="add_subject"),
    path('superadmindash/view-subject',views.view_subject,name="view_subject"),
    path('superadmindash/edit-subject/<int:id>',views.edit_subject,name="edit_subject"),
    path('superadmindash/delete-subject/<int:id>',views.delete_subject,name="delete_subject"),

    # superadmin - teacher urls
    path('superadmindash/add-teacher',views.add_teacher,name="add_teacher"),
    path('superadmindash/add-teachers',views.add_bulkteacher,name="add_bulk_teacher"),
    path('superadmindash/view-teacher',views.view_teacher,name="view_teacher"),
    path('superadmin/edit-teacher/<int:id>',views.edit_teacher,name="edit_teacher"),
    path('superadmin/delete-teacher/<int:id>',views.delete_teacher,name="delete_teacher"),

    # superadmin - student urls
    path('superadmindash/add-student',views.add_student,name="add_single_student"),
    path('superadmindash/add-students',views.add_bulkstudent,name="add_bulk_student"),
    path('superadmindash/view-student',views.view_student,name="view_student"),
    path('superadmindash/edit-student / <str:enrollment_no>',views.edit_student,name="edit_student"),
    path('superadmindash/delete-student / <str:enrollment_no>',views.delete_student,name="delete_student"),

    # superadmin - studymaterial urls
    path('superadmindash/upload-study-material',views.upload_study_material,name="upload_study_material"),
    path('superadmindash/view-study-material',views.view_study_material,name="view_study_material"),
    path('superadmindash/edit-study-material / <int:id>',views.edit_study_material,name="edit_study_material"),
    path('superadmindash/delete-study-material / <int:id>',views.delete_study_material,name="delete_study_material"),


    # superadmin - task urls
    path('superadmindash/add-task',views.add_task,name="add_task"),
    path('superadmindash/view-task',views.view_task,name="view_task"),
    path('superadmindash/edit-task / <int:id>',views.edit_task,name="edit_task"),
    path('superadmindash/delete-task / <int:id>',views.delete_task,name="delete_task"),

    # superadmin - test urls
    path('superadmindash/add-test',views.add_test,name="add_test"),
    path('superadmindash/view-test',views.view_test,name="view_test"),
    path('superadmindash/test-result',views.test_result,name="test_result"),
    path('superadmindash/question-bank/<int:id>',views.question_bank,name="question_bank"),
    path('superadmindash/bulk-question/<int:id>',views.bulk_question,name="bulkquestion_bank"),
    path('superadmindash/edit-test/<int:id>',views.edit_test,name="edit_test"),
    path('superadmindash/delete-test/<int:id>',views.delete_test,name="delete_test"),

    # superadmin - attendance urls
    path('superadmindash/student-attendance',views.student_attendance,name="student_attendance"),
    path('superadmindash/attendance-report',views.attendance_report,name="attendance_report"),
    path('superadmindash/attendance',views.save_method,name="save_attendance"),


    # superadmin - class urls
    path('superadmindash/add-class',views.add_class,name="add_class"),
    # path('superadmindash/view-class',views.view_class,name="view_class"),
    path("superadmin/online-classes/schedule/",views.superadmin_schedule_class,name="superadmin_schedule_class"),
    path("teacher/online-classes/schedule/",views.teacher_schedule_class,name="teacher_schedule_class"),
    path("teacher/online-classes/delete/<int:id>/",views.delete_class,name="delete_class"),
    

    # suparadmin - announcement/notification urls
    path('superadmindash/announcements',views.announcements,name="announcements"),
    path('superadmindash/notification',views.notification,name="notification"),


    # Teacher urls 
    path('teacher',views.teacherdash,name="teacherdash"),

    # teacher - session urls
    path('teacher/session',views.t_current_session,name="t_current_session"),

    # teacher - courses urls
    path('teacher/courses',views.t_my_courses,name="t_my_courses"),

    # teacher - subjects urls
    path('teacher/subjects',views.t_my_subjects,name="t_my_subjects"),

    # teacher - study material urls
    path('teacher/upload-study-material',views.t_upload_sm,name="t_upload_sm"),
    path('teacher/view-study-material',views.t_view_sm,name="t_view_sm"),
    path('teacher/edit-study-material / <int:id>',views.t_edit_sm,name="t_edit_sm"),
    path('teacher/delete-study-material / <int:id>',views.t_delete_sm,name="t_delete_sm"),

    # teacher - tasks urls
    path('teacher/add-task',views.t_add_task,name="t_add_task"),
    path('teacher/view-task',views.t_view_task,name="t_view_task"),
    path('teacher/edit-task/<int:id>',views.t_edit_task,name="t_edit_task"),
    path('teacher/delete-task/<int:id>',views.t_delete_task,name="t_delete_task"),

    # teacher - submission urls
    path('teacher/submission',views.t_submission,name="t_submission"),

    # teacher - test urls
    path('teacher/add-test',views.t_add_test,name="t_add_test"),
    path('teacher/view-test',views.t_view_test,name="t_view_test"),
    path('teacher/question-bank/<int:id>',views.t_question_bank,name="t_question_bank"),
    path('teacher/bulk-question/<int:id>',views.t_bulk_question,name="t_bulkquestion_bank"),
    path('teacher/edit-test/<int:id>',views.t_edit_test,name="t_edit_test"),
    path('teacher/delete-test/<int:id>',views.t_delete_test,name="t_delete_test"),

    # teacher - result urls
    path('teacher/result',views.t_result,name="t_result"),

    # teacher - attendance urls
    path('teacher/mark-attendance',views.t_mark_attendance,name="t_mark_attendance"),
    path('teacher/attendance',views.t_save_method,name="t_save_attendance"),

    # teacher - report urls
    path('teacher/attendance-report',views.t_report,name="t_report"),

    # teacher - classes urls
    path('teacher/add-class',views.t_add_class,name="t_add_class"),
    path('teacher/view-classes',views.t_view_class,name="t_view_class"),

    # teacher - announcements urls
    path('teacher/announcements',views.t_announcements,name="t_announcements"),

    # teacher - notification urls
    path('teacher/notifications',views.t_notifications,name="t_notifications"),

    # teacher - profile urls
    path('teacher/profile',views.t_profile,name="t_profile"),



    # student urls
    path('studentdash',views.studentdash,name='studentdash'),

    # student - session urls
    path('studentdash/session',views.s_current_session,name='s_current_session'),

    # student -course urls
    path('studentdash/courses',views.s_course_detail,name='s_course_detail'),

    # student - subjects urls
    path('studentdash/subjects',views.s_my_subjects,name='s_my_subjects'),

    # student - study material urls
    path('studentdash/study-material',views.s_study_material,name='s_study_material'),

    # student - assignments urls
    path('studentdash/assignments',views.s_assignments,name='s_assignments'),
    path('studentdash/task-submit/<int:id>',views.task_submit,name='s_task_submit'),

    # student - submission urls
    path('studentdash/submissions',views.s_submission,name='s_submission'),

    # student - programming lab urls
    path('studentdash/programming-lab',views.s_programming_lab,name='s_programming_lab'),

    # student - test urls
    path('studentdash/online-tests',views.s_online_test,name='s_online_test'),

    # path('studentdash/online-tests-start/<int:id>',views.test_dt,name='test_dt'),
    path('studentdash/online-tests-start/<int:id>',views.start_test,name='test_dt'),

    # student - results urls
    path('studentdash/results',views.s_my_results,name='s_my_results'),

    # student - attendance urls
    path('studentdash/attendance',views.s_attendance,name='s_attendance'),

    # student - classes urls
    path('studentdash/classes',views.s_class_schedule,name='s_class_schedule'),

    # student - announcements urls
    path('studentdash/announcements',views.s_announcements,name='s_announcements'),

    # student - notifications urls
    path('studentdash/notifications',views.s_notifications,name='s_notifications'),

    # student - profile urls
    path('studentdash/profile',views.s_profile,name='s_profile'),

    # student - help urls
    path('studentdash/help',views.s_help,name='s_help'),


    # logout urls
    path('logout/',views.logout_view,name='logout'),



    # path("onlineclass",views.add_class, name="add_class"),
#   path("superadmin/online-classes/schedule/",views.superadmin_schedule_class,name="superadmin_schedule_class"),
#   path("teacher/online-classes/schedule/",views.teacher_schedule_class,name="teacher_schedule_class"),


   # =================================================
    # ADMIN
    # =================================================
    
    # =================================================
    # GOOGLE CONNECT
    # =================================================

    path(
        "google/login/",
        views.google_login,
        name="google_login"
    ),

    path(
        "google/callback/",
        views.google_callback,
        name="google_callback"
    ),

    # =================================================
    # SCHEDULE MEETING
    # =================================================

    path(
        "schedule-meeting/",
        views.schedule_meeting,
        name="schedule_meeting"
    ),

    # =================================================
    # START CLASS
    # =================================================

    path(
        "meeting/<int:id>/start/",
        views.start_meeting,
        name="start_meeting"
    ),

    # =================================================
    # STUDENT CLASSES
    # =================================================

    path("teacher/classes/", views.teacher_meetings, name="teacher_classes"),
  path("superadmin/classes/", views.superadmin_meetings, name="superadmin_classes"),

    path(
        "student/classes/",
        views.student_classes,
        name="student_classes"
    ),

    # =================================================
    # JOIN MEETING
    # =================================================

    path(
        "meeting/<int:id>/join/",
        views.join_meeting,
        name="join_meeting"
    ),





path(
        'code-lab/',
        views.student_code_lab,
        name='student_code_lab'
    ),
path(
    'run-code/',
    views.run_student_code,
    name='run_student_code'
),





]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


