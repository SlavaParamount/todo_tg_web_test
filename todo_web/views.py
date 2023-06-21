from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models import Task, TelegramUser
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        telegram_user = User(username=username)
        telegram_user.password = make_password(password)
        telegram_user.save()
        print("Register success")
        login(request, telegram_user)
        print("login success")
        return redirect('login')
    return render(request, 'registration.html')

def task_list(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            task_text = request.POST.get('task_text')
            if task_text:
                task = Task.objects.create(user=request.user, title=task_text)
                task.save()
                return redirect('task_list')
        tasks = Task.objects.filter(user=request.user)
        username = request.user.username
        return render(request, 'task_list.html', {'name': username, 'tasks': tasks})
    else:
        return render(request, 'login.html', {'alert_message': "Требуется логин!"})
    
@login_required
def task_list_api(request):
    if request.method == 'POST':
        task_text = request.POST.get('task_text')
        if task_text:
            task = Task.objects.create(user=request.user, title=task_text)
            task.save()
            return HttpResponse(status=201)

    tasks = Task.objects.filter(user=request.user)
    data = serializers.serialize('json', tasks)
    return HttpResponse(data, content_type='application/json')

@require_POST
def update_task(request):
    task_id = request.POST.get('task_id')
    is_completed = bool(request.POST.get('is_completed'))

    try:
        task = Task.objects.get(id=task_id, user=request.user)
        task.is_completed = is_completed
        task.save()
    except Task.DoesNotExist:
        return HttpResponseBadRequest('Invalid task')

    return HttpResponse()

@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')