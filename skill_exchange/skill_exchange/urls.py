"""
URL configuration for skill_exchange project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from exchange import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/',views.register,name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('skills/', views.skills, name='skills'),
    path('add-skill/', views.add_skill, name='add_skill'),
    path('find-students/', views.find_students, name='find_students'),
    path('student-profile/<int:student_id>/', views.student_profile, name='student_profile'),
    path('send-exchange-request/<int:student_id>/', views.send_exchange_request, name='send_exchange_request'),
    path('exchange-requests/',views.exchange_requests,name='exchange_requests'),
    path('logout/', views.logout_view, name='logout'),
    path( 'accept-exchange-request/<int:request_id>/', views.accept_exchange_request, name='accept_exchange_request' ),
    path( 'reject-exchange-request/<int:request_id>/', views.reject_exchange_request, name='reject_exchange_request' ),
    path( 'send-message/<int:student_id>/', views.send_message, name='send_message' ),
    path('messages/', views.messages_list, name='messages_list'),
    path( 'messages/<int:student_id>/', views.messages_view, name='messages' ),
    path( 'learning-sessions/', views.learning_sessions, name='learning_sessions' ),
    path( 'create-session/<int:student_id>/', views.create_session, name='create_session' ),
    path( 'add-rating/<int:student_id>/', views.add_rating, name='add_rating' ),
    path('block-student/<int:student_id>/',views.block_student,name='block_student'),
    path('report-student/<int:student_id>/',views.report_student,name='report_student'),
    path('notifications/', views.notifications, name='notifications'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('my-reviews/', views.my_reviews, name='my_reviews'),
    path('accept-session/<int:session_id>/',views.accept_session,name='accept_session'),
    path('reject-session/<int:session_id>/',views.reject_session, name='reject_session'), 
    path('cancel-session/<int:session_id>/',views.cancel_session,name='cancel_session'),

    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    

