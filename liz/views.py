from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy

from django.views.generic import FormView
# , View 
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth import login, authenticate  
from liz.forms import EmployeeCreationForm  
from liz.models import Employee, Question, Answer, EmployeeAnswer

class RegisterView(FormView):  
  
    form_class = UserCreationForm  
  
    def form_valid(self, form):  
        form.save()  
        username = form.cleaned_data.get('username')  
        raw_password = form.cleaned_data.get('password')  
        login(self.request, authenticate(username=username, password=raw_password))  
        return super(RegisterView, self).form_valid(form)  
  
  
class CreateUserProfile(FormView):  
  
    form_class = EmployeeCreationForm  
    template_name = 'profile-create.html'
    success_url = reverse_lazy('index')  
  
    def dispatch(self, request, *args, **kwargs):  
        if self.request.user.is_anonymous:  
            return HttpResponseRedirect(reverse_lazy('login'))  
        return super(CreateUserProfile, self).dispatch(request, *args, **kwargs)  
  
    def form_valid(self, form):  
        instance = form.save(commit=False)  
        instance.user = self.request.user  
        instance.save()  
        return super(CreateUserProfile, self).form_valid(form)

def index(request):
    context = {}
    if request.user.is_authenticated:  
        context['username'] = request.user.username
        context['usertype'] = Employee.objects.get(user_name=request.user).user_type 
        quests = Question.objects.all()
        variants = Answer.objects.all() 
        context['variants'] = list(variants)
        context['quests'] = list(quests)
        
    return render(request, 'index.html', context) 

# class UserAnswer(View):
#     model = EmployeeAnswer

def answer(request):
    if request.method == 'POST':
        user_id = request.user.id
        user =  Employee.objects.get(user_name=request.user)
        question_id = request.POST["question_id"]
        if 'answer1' in request.POST:
            answer1 = request.POST['answer1']
        if 'answer2' in request.POST:
            answer2 = request.POST['answer2']
        if 'answer3' in request.POST:
            answer3 = request.POST['answer3']
        if 'answer4'in request.POST:
            answer4 = request.POST['answer4']
    right_id = Employee.objects.get(user_name_id=user_id).id
    employee_answer = EmployeeAnswer.objects.get(questions_id=question_id)
    employee_answer.users = user
    # employee_answer.questionnaires='Общий'
    # employee_answer = EmployeeAnswer(questions_id=question_id, user_answer=answer1)

    # employee_answer.user_answer = answer
    employee_answer.save()

    return redirect('index')

# def login(request):  
#     if request.method == 'POST':  
#         form = AuthenticationForm(request=request, data=request.POST)  
#         if form.is_valid():  
#             auth.login(request, form.get_user())  
#             return HttpResponseRedirect(reverse_lazy('registration'))  
#     else:  
#         context = {'form': AuthenticationForm()}  
#         return render(request, 'login.html', context)  
  
  
# def logout(request):  
#     auth.logout(request)  
#     return HttpResponseRedirect(reverse_lazy('registration'))
