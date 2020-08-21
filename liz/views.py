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
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

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

# def index(request):
#     context = {}
#     if request.user.is_authenticated:  
#         context['username'] = request.user.username
#         context['usertype'] = Employee.objects.get(user_name=request.user).user_type 
#         quests = Question.objects.all()
#         variants = Answer.objects.all() 
#         questionnaires = Questionnaire.objects.all()
        
#         appoint = AppointTo.objects.filter(date_finish__gt=datetime.today().date(), users=request.user)
#         context['appoint'] = appoint
#         context['quests'] = quests
#         context['variants'] = variants
#         context['questionnaires'] = questionnaires
#     return render(request, 'index.html', context) 



class ShowQuestionnaires(TemplateView):
    
    template_name = 'index.html'

    def get_context_data(self,  **kwargs):
        if self.request.user.is_authenticated:  
            context = super().get_context_data(**kwargs)
            user_id = self.request.user.id
            appointments = AppointTo.objects.filter(date_finish__gt=datetime.today().date(), users__user_name_id=user_id)
            context['appointments'] = appointments
            context['username'] = self.request.user.username
            if appointments.first():
                context["is_available"] = " Ваши ДОПРОСИКИ: "
            else:
                context["is_available"] = " Вам не назначен ни один ДОПРОСИК или ваше время истекло "  
            return context

class DetailQuestion(DetailView):
    template_name = "question.html"
    model = Question
    slug_url_kwarg = 'question_id_'
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            quest_id = self.object.id
            user_id = self.request.user.id         
            right_id = Employee.objects.get(user_name_id=user_id).id
            questionnaire_id = self.kwargs["questionnaire_id_"]
            context = super().get_context_data(**kwargs)
            variants = Answer.objects.filter(questions_id=quest_id)
            employee_answers = EmployeeAnswer.objects.filter(users__user_name_id=user_id, questionnaires_id=questionnaire_id, questions_id=quest_id)
            time_for_answer = variants.filter(is_right_variant=True).first().time_for_answer
            context['employee_answers'] = employee_answers
            context['time_for_answer'] = time_for_answer
            context['question_id'] = self.kwargs["question_id_"]
            context['questionnaire_id'] = questionnaire_id
            context['variants'] = variants
            context['quest'] = self.object        
            time_start = str(datetime.now()) 
            context['time_start'] = time_start
            context['username'] = self.request.user.username
            
            return context
        else:            
            redirect('index')

class DetailQuestionnaire(DetailView):

    # queryset = Questionnaire.objects.filter(country="Russia")
    # form_class = QuestionnaireForm
    # context_object_name = 'questionnaire'
    template_name = 'questionnaire.html'
    # template_name = 'index.html'
    model = Questionnaire
    form_class = QuestionnaireForm # не рабтает!
    slug_url_kwarg = 'questionnaire_id_'
    slug_field = 'id'
   

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            questionnaire_id = self.object.id
            user_id = self.request.user.id 
            right_id = Employee.objects.get(user_name_id=user_id).id
            appoint = AppointTo.objects.get(users_id=right_id, questionnaires_id=self.object.id) 
            if appoint.isOpen:
                context = super().get_context_data(**kwargs)
                dict_questionnaire = Answer.ditails_qestionnaire(questionnaire_id, right_id)
                context['weight_questionnaire'] = dict_questionnaire["weight_questionnaire"]
                context['variants'] = dict_questionnaire["variants"] 
                context['employee_answers'] = dict_questionnaire["employee_answers"]
                context['list_answered'] = dict_questionnaire["list_answered"]
                # date_finish = self.request.POST.date_finish !!! приходит с index.html не POST запрс
                context['username'] = self.request.user.username
                context['quests'] = dict_questionnaire["quests"]
                # context['date_finish'] = date_finis
                return context
            else:
                redirect('http://127.0.0.1:8000')
        else:            
            redirect('index')


# def details(request, id_):
#     context = {}
#     if request.user.is_authenticated:  
#         context['username'] = request.user.username
#         context['usertype'] = Employee.objects.get(user_name=request.user).user_type 
#         quests = Question.objects.all()
#         variants = Answer.objects.all() 
#         questionnaires = Questionnaire.objects.all()
#         if id_.isdigit() :
#             context['id_'] = int(id_)
#         context['quests'] = quests
#         context['variants'] = variants
#         context['questionnaires'] = questionnaires
    
#     return render(request, 'questionnaire.html', context) 

def answer(request, questionnaire_id_):
    if request.method == 'POST':
        question_id = request.POST["question_id"]
        questionnaire_id = request.POST["questionnaire_id"]
        user_id = request.user.id
        # right_id = Employee.objects.get(user_name_id=user_id).id
        user_name =  Employee.objects.get(user_name=request.user)
        is_answered = EmployeeAnswer.objects.filter(users=user_name, questionnaires=questionnaire_id, questions=question_id)
        for is_answer in is_answered:
            if is_answer is not None:
                return redirect('question_details', questionnaire_id_=questionnaire_id, question_id_=question_id )
        else:
            right_variants = Answer.get_rightlist(request)
            time_ok = EmployeeAnswer.check_time(request)   
            if 'answer_one' in request.POST:
                answer = request.POST['answer_one']
                EmployeeAnswer.save_answer(request, answer, right_variants, time_ok) 
            if 'answer1' in request.POST:
                answer = request.POST['answer1']
                EmployeeAnswer.save_answer(request, answer, right_variants, time_ok) 
            if 'answer2' in request.POST:
                answer = request.POST['answer2']
                EmployeeAnswer.save_answer(request, answer, right_variants, time_ok) 
            if 'answer3' in request.POST:
                answer = request.POST['answer3']
                EmployeeAnswer.save_answer(request, answer, right_variants, time_ok) 
            if 'answer4'in request.POST:
                answer = request.POST['answer4']
                EmployeeAnswer.save_answer(request, answer, right_variants, time_ok)    
            # return HttpResponseRedirect(reverse_lazy('details'))
            # return redirect('index')
            return redirect('question_details', questionnaire_id_=questionnaire_id, question_id_=question_id )

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

# <script defer src="timer.js"></script>