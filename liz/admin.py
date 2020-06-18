from django.contrib import admin
from liz.models import Employee, EmployeeAnswer, Question, QuestionnaireType, RightAnswer, QuestionnaireContent

# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    
    @staticmethod
    def user_name(obj):
        return obj.Employee.user_name

    list_display = ('user_name', 'user_type', )
    fields = ('user_name', 'user_type', 'department')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'image')

@admin.register(QuestionnaireType)
class QuestionnaireTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(QuestionnaireContent)
class QuestionnaireContentAdmin(admin.ModelAdmin):
    pass
    # list_display = ('')

@admin.register(RightAnswer)
class RightAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeAnswer)
class EmployeeAnswerAdmin(admin.ModelAdmin):
    pass
