"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views


urlpatterns = [

    

    path('profile/', views.profile),
   
    path('accounts/',views.accounts),
    path('add-account/',views.add_account),
    path('approve-account/',views.approve_account),
   
   

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    #### quizlite
    path("dashboard", views.dashboard),
    path("", views.landing_page, name="landing_page"),
    path('questions/', views.questions, name="questions"),
    path('question-papers/', views.question_papers, name='question_papers'),
    path('add-to-question-paper/', views.add_to_question_paper, name='add_to_question_paper'),
    
    path('update-question-paper/', views.update_question_paper, name="update_question_paper"),
    path('set-question-paper/', views.set_question_paper, name="set_question_paper"),
    path('questions-discovery/', views.questions_discovery, name="questions_discovery"),
    path('add-question/', views.add_question, name="add_question"),

    path('auth/google', views.google_callback),
    path('inquiry', views.inquiry),
    path('take-exam', views.take_exam),
    path('start-exam/', views.start_exam),
    path('save-answer/', views.save_answer),
    path('save-final-sheet/', views.save_final_sheet),
    path('student-answer-sheet/', views.student_answer_sheet),
    path('explanation-sheet/', views.explanation_sheet),

    path('students/', views.students, name="students"),
    path('get-student/<str:student_id>/', views.get_student, name="get_student"),
    path('delete-student/<str:student_id>/', views.delete_student, name="delete_student"),
    path('edit-student/<str:student_id>/', views.edit_student, name='edit_student'),


 
    path('classes/', views.classes, name='classes'),
    path('get-class/<str:class_id>/', views.get_class, name='get_class'),
    path('delete-class/<str:class_id>/', views.delete_class, name='delete_class'),
    path('list-classes/', views.list_classes, name='list_classes'),

    path('teachers/', views.teachers, name='teachers'),
    path('delete-teacher/<str:teacher_id>/', views.delete_teacher, name='delete_teachers'),
    path('get-teacher/<str:teacher_id>/', views.get_teacher, name='get_teacher'),
    path('edit-teacher/<str:teacher_id>/', views.edit_teacher, name='edit_teacher'),

    path('review-qp/<str:qp_temp_id>/', views.review_qp, name="review_qp"),
    path('view-qp/<str:qp_temp_id>/', views.view_qp, name='view_qp'),
    path('questions/<str:qid>/', views.question_details, name='question_details'),
    
    path('analytics-index/', views.analytics_index, name="analytics_index"),
    path('analytics-dashboard-crm/', views.analytics_dashboard_crm, name="analytics_dashboard_crm"),
    path('analytics-dashboard-projects/', views.analytics_dashboard_projects, name="analytics_dashboard_projects"),
    path('blog_page/', views.blog_page, name="blog_page"),
    
    
    ]

