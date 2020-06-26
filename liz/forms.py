from django import forms  
from liz.models import Employee

class EmployeeCreationForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['department', 'user_type']