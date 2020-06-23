from django.contrib import admin
from liz.models import User, Employee, Question,  EmployeeAnswer, Questionnaire
#from liz.models import EmployeeAnswer,  QuestionnaireContent, QuestionnaireResult
from liz.models import AppointTo

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    
    @staticmethod
    def user_name(obj):
        return obj.Employee.user_name

    list_display = ('user_name', 'user_type', )
    fields = ('user_name', 'user_type', 'department')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'image', 'answer_right', 'answer_weight')


@admin.register(EmployeeAnswer)
class EmployeeAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    pass
    

@admin.register(AppointTo)
class AppointToAdmin(admin.ModelAdmin):
    list_display = ('users', 'questionnaires', 'date_start', 'date_finish' )

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

