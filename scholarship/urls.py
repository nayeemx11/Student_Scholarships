from django.urls import path
from . import views

urlpatterns = [
    path('update_student_info/', views.update_student_info, name='update_student_info'),
    
    # is matching with reg
    path('verify_student/', views.verify_student, name='verify_student'),
    
    path('message/', views.message, name='message'),
    
    path('comm_home/', views.comm_home, name='comm_home'),
    
    path('view_application/', views.view_application, name='view_application'),
    
    path('view_applicant/', views.view_applicant, name='view_applicant'),
    
    path('selected_applicant/', views.selected_applicant, name='selected_applicant'),
    
    path('info_send/<int:application_id>', views.info_send, name='info_send'),
    
    path('award_send/<int:student_identity_number>', views.award_send, name='award_send'),
    
    path('awarded_student', views.awarded_student, name='awarded_student'),
    
    # this is for application
    path('apply_scholarship/', views.apply_scholarship, name='apply_scholarship'),
    
    path('award_scholarship', views.award_scholarship, name='award_scholarship'),
    path('send_mail_to_awarded_student/', views.send_mail_to_awarded_student, name='send_mail_to_awarded_student'),
    path('notify_other_eligible/', views.notify_other_eligible_applicants, name='notify_other_eligible_applicants'),
    path('committee_dashboard/', views.committee_dashboard, name='committee_dashboard'),
]