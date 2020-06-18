from django.shortcuts import render

from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy

from django.views.generic import FormView  
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth import login, authenticate  
from liz.forms import EmployeeCreationForm  
from liz.models import Employee, Question

class RegisterView(FormView):  
  
    form_class = UserCreationForm  
  
    def form_valid(self, form):  
        form.save()  
        username = form.cleaned_data.get('username')  
        raw_password = form.cleaned_data.get('password1')  
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
        # context['usertype'] = Employee.objects.get(user_name=request.user).user_type  
        context['quests'] = list(Question.objects.all())
    return render(request, 'index.html', context) 



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
