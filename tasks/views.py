from django.shortcuts import render,redirect
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout

# Create your views here.
def task_list(request):
    task = Task.objects.all()
    
    
    context = {
        'tasks' : task
    }
    return render(request,'tasks/task_list.html',context)

def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        Task.objects.create(
            user = request.user,
            title = title,
            description = description
        )
        
        return redirect('task_list')
        
    
    return render(request, 'tasks/task_form.html')

def edit_task(request,task_id):
    task = Task.objects.get(id=task_id)
    
    task.completed = True
    task.save()
    
    return redirect('task_list')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        
        user = User.objects.create_user(
            username = username,
            email = email,
            password = password
        
        )
        login(request,user)
        
        return redirect('task_list')
    return render(request , 'task/register.html')