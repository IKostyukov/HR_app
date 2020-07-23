"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from liz.views import RegisterView, CreateUserProfile, ShowQuestionnaires,  answer
# , index, details
from liz.views import DetailQuestionnaire
 #, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy 
from django.conf.urls.static import static
from django.conf import settings     

app_name = 'app'  

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', index, name='index'),
    path('', ShowQuestionnaires.as_view(), name='index'),
    path('questionnaire/details', answer, name='good'),
    path('questionnaire/inp', answer, name='good'),
    path('questionnaire/<id_>', DetailQuestionnaire.as_view(), name='details'),
    # path('questionnaire/<id_>', details, name='details'),
    path('login/', LoginView.as_view(), name='login'),  
	path('logout/', LogoutView.as_view(), name='logout'), 
    path('register/', RegisterView.as_view(  
        template_name='register.html',  
		success_url=reverse_lazy('profile-create')  
    ), name='register'),  
    path('profile-create/', CreateUserProfile.as_view(), name='profile-create'), 
      
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)