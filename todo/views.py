from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from .forms import NewUserForm, AuthForm, TaskForm, CategoryForm
from .models import User, Category, Task
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from datetime import date, datetime

current_time = datetime.now().strftime("%H:%M:%S")


@login_required
def user_dashboard(request, id):
    user = get_object_or_404(User, pk=id)
    category = Category.objects.filter(user=user)
    task = Task.objects.all()

    # get the total count for completed, pending and overdue tasks
    completed = Task.objects.filter(category__in=category, is_complete='yes', is_deleted='no').count()
    pending = Task.objects.filter(category__in=category, is_complete="no", is_deleted="no") \
        .filter(Q(time__gte=current_time) & Q(due_date__gte=date.today()) | Q(due_date__isnull=True)).count()
    overdue = Task.objects.filter(category__in=category, is_deleted='no', is_complete='no') \
        .filter(Q(time__lt=current_time) & Q(due_date=date.today()) | Q(due_date__lt=date.today())).count()

    return render(request, 'todo/user_dashboard.html', {
        'user': user,
        'category': category,
        'task': task,
        'completed': completed,
        'pending': pending,
        'overdue': overdue,
    })


def user_registration(request):
    message = ''
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            message = "Registration successful."
        else:
            form.errors
            message = form.errors
    form = NewUserForm
    return render(request, "todo/user_registration.html", {"register_form": form, 'message': message})


def user_login(request):
    message = ''
    if request.method == "POST":
        form = AuthForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/user_dashboard/' + str(int(user.id)))
            else:
                message = "Invalid username or password."
        else:
            message = "Invalid username or password."

    form = AuthForm()
    return render(request, "todo/user_login.html", {"login_form": form, 'message': message})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


@login_required
def task_list(request, id):
    # get the object using the id
    category = get_object_or_404(Category, pk=id)
    user = get_object_or_404(User, pk=category.user_id)
    # filters all the tasks that belong to a specific category
    tasks = Task.objects.filter(category=category, is_complete="no", is_deleted="no").order_by('due_date')

    return render(request, 'todo/task_list.html', {
        'user': user,
        'category': category,
        'tasks': tasks
    })


@login_required
def new_task(request, id):
    title = "CREATE TASK"
    # get the object using the id
    category = get_object_or_404(Category, pk=id)
    user = get_object_or_404(User, pk=category.user_id)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            myTask = form.save(commit=False)
            myTask.is_complete = "no"
            myTask.is_deleted = "no"
            myTask.category_id = id
            myTask.save()

            return redirect('/task_list/' + str(int(category.id)))
        else:
            return HttpResponse(form.errors.values())
    else:
        form = TaskForm()
    return render(request, 'todo/task.html', {
        'user': user,
        'title': title,
        'form': form,
        'category': category,
    })


@login_required
def update_task(request, id):
    title = "UPDATE TASK"
    # get the object using the id
    task = get_object_or_404(Task, pk=id)
    category = get_object_or_404(Category, pk=task.category_id)
    user = get_object_or_404(User, pk=category.user_id)
    if request.method == "POST":
        # get all the data of that specific task
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/task_list/' + str(int(category.id)))
        else:
            return HttpResponse(form.errors.values())
    else:
        form = TaskForm(instance=task)
        return render(request, 'todo/task.html', {
            'user': user,
            'title': title,
            'task': task,
            'category': category,
            'form': form,
        })


@login_required
def delete_task(request, id):
    # get the object using the id
    task = get_object_or_404(Task, pk=id)
    # get category object of the specified task
    category = get_object_or_404(Category, pk=task.category_id)

    # change the value of is_deleted to yes
    form = TaskForm(instance=task)
    myTask = form.save(commit=False)
    myTask.is_deleted = "yes"
    myTask.save()

    return redirect('/task_list/' + str(int(category.id)))


@login_required
def mark_as_done_task(request, id):
    # get the object using the id
    task = get_object_or_404(Task, pk=id)
    # get category object of the specified task
    category = get_object_or_404(Category, pk=task.category_id)

    # change the value of is_completed to yes
    form = TaskForm(instance=task)
    myTask = form.save(commit=False)
    myTask.is_complete = "yes"
    myTask.save()

    return redirect('/task_list/' + str(int(category.id)))


@login_required
def new_category(request, id):
    title = "CREATE CATEGORY"
    # get the object using the id
    user = get_object_or_404(User, pk=id)
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            myCateg = form.save(commit=False)
            myCateg.user_id = id
            myCateg.save()
            return redirect('/user_dashboard/' + str(int(user.id)))
        else:
            return HttpResponse(form.errors.values())
    else:
        form = CategoryForm()
        return render(request, 'todo/category.html', {
            'title': title,
            'user': user,
            'form': form
        })


@login_required
def update_category(request, id):
    title = "UPDATE CATEGORY"
    # get the object using the id
    category = get_object_or_404(Category, pk=id)
    user = get_object_or_404(User, pk=category.user_id)
    if request.method == "POST":
        # get all the data of that specific category
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('/user_dashboard/' + str(int(category.user_id)))
        else:
            return HttpResponse(form.errors.values())
    else:
        form = CategoryForm(instance=category)
        return render(request, 'todo/category.html', {
            'user': user,
            'title': title,
            'form': form
        })


@login_required
def delete_category(request, id):
    # get the object using the id
    category = get_object_or_404(Category, pk=id)
    user = get_object_or_404(User, pk=category.user_id)
    # delete in db
    category.delete()
    return redirect('/user_dashboard/' + str(int(user.id)))


@login_required
def completed_tasks_list(request, id):
    title = "COMPLETED TASKS"
    # get the object using the id
    user = get_object_or_404(User, pk=id)
    category = Category.objects.filter(user_id=id)
    # get all the tasks that belong to different categories of that specific user
    task = Task.objects.filter(category__in=category, is_complete="yes", is_deleted="no")

    return render(request, "todo/summary_tasks.html", {
        'title': title,
        'user': user,
        'category': category,
        'task': task,
        'completed_tasks_list': True
    })


@login_required
def pending_tasks_list(request, id):
    title = "PENDING TASKS"
    # get the object using the id
    user = get_object_or_404(User, pk=id)
    category = Category.objects.filter(user_id=id)
    # get all the tasks that belong to different categories of that specific user
    task = Task.objects.filter(category__in=category, is_complete="no", is_deleted="no") \
        .filter(Q(time__gte=current_time) & Q(due_date__gte=date.today()) | Q(due_date__isnull=True))\
        .order_by('due_date')

    return render(request, "todo/summary_tasks.html", {
        'title': title,
        'user': user,
        'category': category,
        'task': task,
        'pending_tasks_list': True
    })


@login_required
def overdue_tasks_list(request, id):
    title = "OVERDUE TASKS"
    # get the object using the id
    user = get_object_or_404(User, pk=id)
    category = Category.objects.filter(user_id=id)
    # get all the tasks that belong to different categories of that specific user
    task = Task.objects.filter(category__in=category, is_deleted='no', is_complete='no') \
        .filter(Q(time__lt=current_time) & Q(due_date=date.today()) | Q(due_date__lt=date.today()))

    return render(request, "todo/summary_tasks.html", {
        'title': title,
        'user': user,
        'category': category,
        'task': task,
        'overdue_tasks_list': True
    })


@login_required
def mark_as_undone_task(request, id):
    # get the object using the id
    task = get_object_or_404(Task, pk=id)
    # get category object of the specified task
    category = get_object_or_404(Category, pk=task.category_id)

    # change the value of is_completed to no
    form = TaskForm(instance=task)
    myTask = form.save(commit=False)
    myTask.is_complete = "no"
    myTask.save()

    return redirect('/completed_tasks_list/' + str(int(category.user_id)))


@login_required
def completed_delete(request, id):
    # get the object using the id
    task = get_object_or_404(Task, pk=id)
    # get category object of the specified task
    category = get_object_or_404(Category, pk=task.category_id)

    # change the value of id_deleted to yes
    form = TaskForm(instance=task)
    myTask = form.save(commit=False)
    myTask.is_deleted = "yes"
    myTask.save()

    return redirect('/completed_tasks_list/' + str(int(category.user_id)))


@login_required
def pending_done(request, id):
    # get the object using the id
    task = get_object_or_404(Task, pk=id)
    # get category object of the specified task
    category = get_object_or_404(Category, pk=task.category_id)

    # change the value of is_completed to yes
    form = TaskForm(instance=task)
    myTask = form.save(commit=False)
    myTask.is_complete = "yes"
    myTask.save()

    return redirect('/pending_tasks_list/' + str(int(category.user_id)))


@login_required
def pending_delete(request, id):
    # get the object using the id
    task = get_object_or_404(Task, pk=id)
    # get category object of the specified task
    category = get_object_or_404(Category, pk=task.category_id)

    # change the value of is_deleted to yes
    form = TaskForm(instance=task)
    myTask = form.save(commit=False)
    myTask.is_deleted = "yes"
    myTask.save()

    return redirect('/pending_tasks_list/' + str(int(category.user_id)))


@login_required
def overdue_done(request, id):
    # get the object using the id
    task = get_object_or_404(Task, pk=id)
    # get category object of the specified task
    category = get_object_or_404(Category, pk=task.category_id)

    # change the value of is_completed to yes
    form = TaskForm(instance=task)
    myTask = form.save(commit=False)
    myTask.is_complete = "yes"
    myTask.save()

    return redirect('/overdue_tasks_list/' + str(int(category.user_id)))


@login_required
def overdue_delete(request, id):
    # get the object using the id
    task = get_object_or_404(Task, pk=id)
    # get category object of the specified task
    category = get_object_or_404(Category, pk=task.category_id)

    # change the value of is_deleted to yes
    form = TaskForm(instance=task)
    myTask = form.save(commit=False)
    myTask.is_deleted = "yes"
    myTask.save()

    return redirect('/overdue_tasks_list/' + str(int(category.user_id)))
