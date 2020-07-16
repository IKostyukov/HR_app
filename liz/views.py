from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy

from django.views.generic import FormView, DetailView, TemplateView 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate  
from liz.forms import EmployeeCreationForm, QuestionnaireForm   
from liz.models import Employee, Question, Answer, Questionnaire
from liz.models import AppointTo,  EmployeeAnswer
from datetime import datetime

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
        questionnaires = Questionnaire.objects.all()
        
        appoint = AppointTo.objects.filter(date_finish__gt=datetime.today().date(), users=request.user)
        context['appoint'] = appoint
        context['quests'] = quests
        context['variants'] = variants
        context['questionnaires'] = questionnaires
    return render(request, 'index.html', context) 



class ShowQuestionnaires(TemplateView):
    
    template_name = 'index.html'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        appoint = AppointTo.objects.all()
        context['appoint'] = appoint
        context['username'] = self.request.user.username
        context['questionnaires'] = Questionnaire.objects.all()
        return context
    

class DetailQuestionnaire(DetailView):

    # queryset = Questionnaire.objects.filter(country="Russia")
    # form_class = QuestionnaireForm
    # context_object_name = 'questionnaire'
    template_name = 'questlist.html'
    model = Questionnaire
    form_class = QuestionnaireForm # не рабтает!
    pk_url_kwarg = 'pk'
    query_pk_and_slug = True
    slug_url_kwarg = 'id_'
    slug_field = 'id'

    def get_context_data(self,  *arg, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["now"] = timezone.now()   !!!! на будущее !!!!
        # if request.user.is_authenticated:  
            # context['username'] = request.user.username
            # context['usertype'] = Employee.objects.get(user_name=request.user).user_type 
        quests = Question.objects.all()
        variants = Answer.objects.all() 
        questionnaires = Questionnaire.objects.all()
        context['quests'] = quests
        context['variants'] = variants
        context['questionnaires'] = questionnaires
        return context


def details(request, id_):
    context = {}
    if request.user.is_authenticated:  
        context['username'] = request.user.username
        context['usertype'] = Employee.objects.get(user_name=request.user).user_type 
        quests = Question.objects.all()
        variants = Answer.objects.all() 
        questionnaires = Questionnaire.objects.all()
        if id_.isdigit() :
            context['id_'] = int(id_)
        context['quests'] = quests
        context['variants'] = variants
        context['questionnaires'] = questionnaires
    
    return render(request, 'questionnaire.html', context) 

def answer(request):
    if request.method == 'POST':
        question_id = request.POST["question_id"]
        questionnaire_id = request.POST["questionnaire_id"]
        right_variants = []
        variants = Answer.objects.filter(questions_id=question_id).filter(is_right_variant=True)
        for ok in variants:
            right_variants.append(ok.variant)
        user_id = request.user.id
        right_id = Employee.objects.get(user_name_id=user_id).id
        user_name =  Employee.objects.get(user_name=request.user)
        questionnaire = Questionnaire.objects.filter(questions__id=question_id) #тест на получение

        #test from
        for qus in questionnaire: 
            print(qus.id)
        ggg = Question.objects.all()
        print(ggg)  

        for g in ggg.filter(questionnaires=questionnaire_id): 
            s = g  
            print(s)
        # test till

        if 'answer1' in request.POST:
            answer = request.POST['answer1']
            employee_answer = EmployeeAnswer(
                users=user_name, 
                questions_id=question_id ,
                questionnaires_id=questionnaire_id, 
                user_answer=answer)
            if answer in right_variants:
                employee_answer.is_correct=True 
                employee_answer.save()
            else:
                employee_answer.save()
        if 'answer2' in request.POST:
            answer = request.POST['answer2']
            employee_answer = EmployeeAnswer(users=user_name, questions_id=question_id, questionnaires_id=questionnaire_id , user_answer=answer)
            if answer in right_variants:
                employee_answer.is_correct=True 
                employee_answer.save()
            else:
                employee_answer.save()
        if 'answer3' in request.POST:
            answer = request.POST['answer3']
            employee_answer = EmployeeAnswer(users=user_name, questions_id=question_id, questionnaires_id=questionnaire_id , user_answer=answer)
            if answer in right_variants:
                employee_answer.is_correct=True 
                employee_answer.save()
            else:
                employee_answer.save()
        if 'answer4'in request.POST:
            answer = request.POST['answer4']
            employee_answer = EmployeeAnswer(users=user_name, questions_id=question_id, questionnaires_id=questionnaire_id , user_answer=answer)
            if answer in right_variants:
                employee_answer.is_correct=True 
                employee_answer.save()
            else:
                employee_answer.save()
        # return HttpResponseRedirect(reverse_lazy('details'))
        # return redirect('index')
        return redirect('details', id_=questionnaire_id)

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
