from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'tasks/home.html')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    
    context = {
        'tasks': tasks
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')
        
        # Fixed: Avoid saving empty strings if dates or priorities are optional in your model
        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            priority=priority if priority else None,
            due_date=due_date if due_date else None
        )
        return redirect('tasks:task_list')
        
    return render(request, 'tasks/task_form.html')


@login_required
def edit_task(request, task_id):
    # Secured: Filters by request.user so users can't edit other people's tasks
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.priority = request.POST.get('priority')
        
        due_date = request.POST.get('due_date')
        task.due_date = due_date if due_date else None
        
        task.save()
        return redirect('tasks:task_list')
    
    # Fixed: Removed the unintentional auto-complete logic that was overriding the edit form rendering
    context = {
        'task': task
    }
    return render(request, 'tasks/task_form.html', context)


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        task.delete()
        return redirect('tasks:task_list')
    
    context = {
        'task': task
    }
    return render(request, 'tasks/task_confirm_delete.html', context)


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    # Note: If your model uses a BooleanField (like completed = True), change this line to: task.completed = True
    task.status = 'completed'
    task.save()
    return redirect('tasks:task_list')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email', '')  # Falls back to empty string if missing
        password = request.POST.get('password')
        
        # Simple validation check to ensure username and password aren't empty
        if not username or not password:
            error_message = "Username and password are required."
            return render(request, 'tasks/register.html', {'error_message': error_message})
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            login(request, user)
            return redirect('tasks:task_list')
        except Exception as e:
            # Captures database errors (like a duplicate username) and shows it cleanly
            error_message = f"Registration failed: {str(e)}"
            return render(request, 'tasks/register.html', {'error_message': error_message})
    
    return render(request, 'tasks/register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('tasks:task_list')
        else:
            error_message = "Invalid username or password"
            return render(request, 'tasks/login.html', {'error_message': error_message})
    
    return render(request, 'tasks/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')  
