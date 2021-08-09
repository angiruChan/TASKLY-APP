from django import forms
from .models import Task, Category, Priority
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# login form
class AuthForm(AuthenticationForm):

    # accept all the argument
    def __init__(self, *args, **kwargs):
        # Calling the parent class's initializer
        super(AuthForm, self).__init__(*args, **kwargs)

    # fields
    username = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username'}))

    password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'password'}))


# registration form
class NewUserForm(UserCreationForm):
    # fields
    email = forms.CharField(label="", widget=forms.TextInput(
         attrs={'class': 'form-control', 'placeholder': 'email'}))
    username = forms.CharField(label="", widget=forms.TextInput(
         attrs={'class': 'form-control', 'placeholder': 'username'}))
    password1 = forms.CharField(label="", widget=forms.PasswordInput(
         attrs={'class': 'form-control', 'placeholder': 'password'}))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(
         attrs={'class': 'form-control', 'placeholder': 'confirm password'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        # verify email
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class TaskForm(forms.ModelForm):

    # modifying the fields
    description = forms.CharField(required=False, label="Description", widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 2}))
    time = forms.TimeField(required=False, label="Time (optional)", widget=forms.TimeInput(
        attrs={'class': 'form-control', 'type': 'time'}))
    due_date = forms.DateField(required=False, label="Due Date (optional)", widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}))
    priority = forms.ModelChoiceField(Priority.objects.all())

    class Meta:
        model = Task
        fields = ("title", "description", "time", "due_date", "priority")


class CategoryForm(forms.ModelForm):

    name = forms.CharField(label="Category Name", widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Category
        fields = {"name"}