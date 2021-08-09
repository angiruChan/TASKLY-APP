from django.urls import path
from . import views

app_name = 'todo'

urlpatterns =[
    path("", views.user_login, name="user_login"),
    path("user_logout/", views.user_logout, name="user_logout"),
    path("user_registration/", views.user_registration, name="user_registration"),
    path("user_dashboard/<int:id>/", views.user_dashboard, name="user_dashboard"),
    path("task_list/<int:id>/", views.task_list, name="task_list"),

    # task functions
    path("new_task/<int:id>/", views.new_task, name="new_task"),
    path("update_task/<int:id>/", views.update_task, name="update_task"),
    path("delete_task/<int:id>/", views.delete_task, name="delete_task"),
    path("mark_as_done_task/<int:id>/", views.mark_as_done_task, name= "mark_as_done_task"),

    # category functions
    path("new_category/<int:id>/", views.new_category, name="new_category"),
    path("update_category/<int:id>/", views.update_category, name="update_category"),
    path("delete_category/<int:id>/", views.delete_category, name="delete_category"),

    # list of tasks according to status
    path("completed_tasks_list/<int:id>/", views.completed_tasks_list, name="completed_tasks_list"),
    path("pending_tasks_list/<int:id>/", views.pending_tasks_list, name="pending_tasks_list"),
    path("overdue_tasks_list/<int:id>/", views.overdue_tasks_list, name="overdue_tasks_list"),

    # task summary actions
    path("mark_as_undone_task/<int:id>/", views.mark_as_undone_task, name="mark_as_undone_task"),
    path("completed_delete/<int:id>/", views.completed_delete, name="completed_delete"),
    path("pending_done/<int:id>/", views.pending_done, name="pending_done"),
    path("pending_delete/<int:id>/", views.pending_delete, name="pending_delete"),
    path("overdue_done/<int:id>/", views.overdue_done, name="overdue_done"),
    path("overdue_delete/<int:id>/", views.overdue_delete, name="overdue_delete"),


]


