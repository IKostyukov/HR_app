from django import forms  
from liz.models import Employee, Questionnaire

class EmployeeCreationForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['department', 'user_type']
        

class QuestionnaireForm(forms.ModelForm):

    question = forms.CharField(widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Questionnaire
        fields = ['title', 'description', 'question']