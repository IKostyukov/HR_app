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
            # right_id = Employee.objects.get(user_name_id=user_id).id
            questionnaires = Questionnaire.objects.filter(
                users__user_name_id=user_id,
                # appoint__date_finish__gt=datetime.today().date()
                )
            is_one_available = AppointTo.objects.filter(date_finish__gt=datetime.today().date(), users__user_name_id=user_id).first()
            if is_one_available:
                context["is_available"] = " Ваши ДОПРОСИКИ: "
            else:
                context["is_available"] = " Вам не назначен ни один ДОПРОСИК или ваше время истекло "
            context['questionnaires'] = questionnaires 
            context['username'] = self.request.user.username
            
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
            context = super().get_context_data(**kwargs)
            variants = Answer.objects.filter(questions_id=quest_id)
            # employee_answer = EmployeeAnswer.objects.filter(users_id=user_id, questionnaires_id=self.object.questionnaires.questionnaires__id, question_id=quest_id)
            # context['employee_answer'] = employee_answer
            context['question_id'] = self.kwargs["question_id_"]
            context['questionnaire_id'] = self.kwargs["questionnaire_id_"]
            context['variants'] = variants
            context['quest'] = self.object
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
                # context["now"] = timezone.now()   !!!! на будущее !!!!
                # if request.user.is_authenticated:  
                
                questionnaire_dict = Answer.count_qestionnaire(questionnaire_id, right_id)
                context['weight_questionnaire'] = questionnaire_dict["weight_questionnaire"]
                context['variants'] = questionnaire_dict["variants"] 
                context['employee_answers'] = questionnaire_dict["employee_answers"]
                context['list_answered'] = questionnaire_dict["list_answered"]
                # date_finish = self.request.POST.date_finish !!! приходит с index.html не POST запрс
                context['username'] = self.request.user.username
                context['quests'] = questionnaire_dict["quests"]
                # context['date_finish'] = date_finish
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
        right_variants = []
        variants = Answer.objects.filter(questions_id=question_id).filter(is_right_variant=True)
        for ok in variants:
            right_variants.append(ok.variant)
        user_id = request.user.id
        right_id = Employee.objects.get(user_name_id=user_id).id
        user_name =  Employee.objects.get(user_name=request.user)

        #test from
        questionnaire = Questionnaire.objects.filter(questions__id=question_id) #тест на получение
        for qus in questionnaire: 
            print(qus.id, "id вопроса получили из Опросника")

        # test till

        # test = get_object_or_404(EmployeeAnswer, users=user_name, user_answer=None)
        
        tests = EmployeeAnswer.objects.filter(users=user_name, questionnaires=questionnaire_id, questions=question_id)
        for test in tests:
            if test is not None:
                print(2, test)
                return redirect('question_details', questionnaire_id_=questionnaire_id, question_id_=question_id )
        else:   
            if 'answer_one' in request.POST:
                answer = request.POST['answer_one']
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
