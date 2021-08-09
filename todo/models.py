from django.db import models
from django.contrib.auth.models import User
import datetime


class Category(models.Model):
    # attributes for category
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Priority(models.Model):
    # attribute for priority
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Task(models.Model):
    # attributes for task   
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True, null=True)  # optional
    time = models.TimeField(blank=True, null=True)  # optional
    due_date = models.DateField(blank=True, null=True)  # optional
    is_complete = models.CharField(max_length=50)
    is_deleted = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # foreign keys
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='task')
    priority = models.ForeignKey(
        Priority, on_delete=models.CASCADE, related_name='task')

    def __str__(self):
        return self.title

    def overdue(self):
        result = ''

        if self.due_date:

            if self.due_date == datetime.date.today() and self.time:
                if self.time < datetime.datetime.now().time():
                    result = "OVERDUE"
            elif self.due_date < datetime.date.today():
                result = "OVERDUE"

        return result
