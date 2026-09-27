from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list,name='task_list'),
    path('register/', views.register,name='register'),
    path('create/', views.create_task,name='create_task'),
    path('complete/<int:task_id>/', views.edit_task, name='complete_task'), 
]
