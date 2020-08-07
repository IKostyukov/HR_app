from django.contrib import admin
from liz.models import User, Employee, Question,  EmployeeAnswer, Questionnaire
#from liz.models import EmployeeAnswer,  QuestionnaireContent, QuestionnaireResult
from liz.models import AppointTo, Answer


admin.site.site_header = "Панель HR-менеджера (Liz)"



class EmployeeAnswerInline(admin.TabularInline):
    model = EmployeeAnswer
    max_num=5
    extra=0

class AppointToInline(admin.TabularInline):
    model = AppointTo
    max_num=4 
    extra=0

class AnswerInline(admin.TabularInline):
    model = Answer
    
    # var_exist = Answer.objects.only('questions)
    # if var_exist.variants:
    #     extra=0
    # else:
    extra=4
    

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    inlines = (AppointToInline,)
    
    @staticmethod
    def correct_name(obj):
        return obj.user_name
    list_display = ('correct_name', 'user_type' )
    fields = ('user_name', 'user_type', 'department')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # @staticmethod
    # def correct_name(obj):
    #     queryset = obj.questionnaires                       
    #     # Questionnaire.objects.filter(title=obj)
    #     # return obj.questionnaires.title
    #     # quest = Questionnaire.objects.prefetch_related(Prefetch('questions', queryset=queryset))
    #     return queryset
    inlines = (AnswerInline, EmployeeAnswerInline, )
    list_display = ('question','image', 'answer_right', 'answer_weight')
    list_filter = ('question_type', 'questionnaires')
    def has_module_permission(self, request):
        return True
    
    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(EmployeeAnswer)
class EmployeeAnswerAdmin(admin.ModelAdmin):
    
    @staticmethod
    def correct_name(self):
        return self.users
        # .user_name
    @staticmethod
    def points(self):
        return 2 # здесь можно вызвать вункцию 
        # их view.py count_qestionnaire
#импортировав её в admin.py
#!!!!!!!!!!!!!!!!!#
    list_display = ('correct_name', 'questionnaires', 'questions', 'user_answer', 'is_correct', 'points' )
    fields = ('users', 'questionnaires', 'questions', 'user_answer', 'is_correct')
    list_filter = ('users', 'questionnaires')

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    inlines = (AppointToInline,)
    list_filter = ('title', 'users', 'questions')

@admin.register(AppointTo)
class AppointToAdmin(admin.ModelAdmin):

    @staticmethod
    def correct_name(obj):
        return obj.users.user_name
    @staticmethod
    def total(obj):
        return 9

    list_display = ('correct_name', 'questionnaires', 'date_start', 'date_finish', 'total')
    fields = ('users', 'questionnaires', 'date_start', 'date_finish')
    list_filter = ('users', 'questionnaires','date_finish')

# @admin.register(QuestionnaireContent)
# class QuestionnaireContentAdmin(admin.ModelAdmin):
#     pass
    # list_display = ('')

# @admin.register(EmployeeAnswer)
# class EmployeeAnswerAdmin(admin.ModelAdmin):
#     pass

# @admin.register(QuestionnaireResult)
# class QuestionnaireResultAdmin(admin.ModelAdmin):
#     pass

