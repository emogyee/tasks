from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.home, name='home'),
    path('task_list/', views.task_list, name='task_list'),
    path('register/', views.register, name='register'),
    path('accounts/login/', views.login_user,name='login'),
    path('logout/', views.logout_user,name='logout'),
    path('create/', views.create_task,name='create_task'),
    path('edit/<int:task_id>/', views.edit_task,name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task,name='delete_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'), 
]
