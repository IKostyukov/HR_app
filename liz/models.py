from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# from django.contrib.postgres.fields import JSONField

ANSWER_IS_TRUE = [
    ('One', 'Один правильный ответ'),
    ('Multi', 'Несколько правильных ответов'),
]

USER_TYPE = [
        ('MG', 'Менеджер'),
        ('CW', 'Сотрудник'), 
        ]

QUESTIONE_TYPE = [
    ('One', 'Один правильный ответ'),
    ('Multi', 'Несколько правильных ответов'),
    ]

class Employee(models.Model):
    MANAGER = 'MG'
    COWORKER = 'CW'    
    user_name = models.OneToOneField(User, 
    null=True, blank=True, 
    on_delete=models.CASCADE, 
    related_name='employee')
    department =  models.CharField(max_length=100)
    user_type = models.CharField(
        max_length=10, 
        choices = USER_TYPE, 
        default = COWORKER,
        null=True, blank=True)

    def __str__(self):
        if self.user_name.username:
            return self.user_name.username

    class Meta:
        verbose_name = "сотрудник"
        verbose_name_plural = "№1: сотрудники"


class Question(models.Model):
    question = models.CharField("Вопрос", max_length=128, null=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d', null=True, blank=True) 
    question_type = models.CharField(max_length=10, 
    choices=(QUESTIONE_TYPE), blank=True, default='One', verbose_name='тип вопросов')
    answer_right = models.CharField("правильные ответы", max_length=128, blank=True, null=True)
    answer_all_variants = models.CharField("варианты ответов (в том числе все правильные)", max_length=128, blank=True, null=True)
    answer_weight = models.SmallIntegerField("баллы", default=0)

    def __str__(self):
        return self.question 
    
    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = '№2: вопросы'

class Answer(models.Model):
    questions = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='вопросы')
    variant = models.CharField("варианты ответа в опроснике", max_length=128,  null=True)
    is_right_variant = models.BooleanField("укажите правильный ли это вариант?")
    answer_weight = models.SmallIntegerField("баллы", default=0)

    def __str__(self):
        return self.variant 
    
    class Meta:
        verbose_name = "вариант для ответа"
        verbose_name_plural = "№6: варианты для ответов"
    
class Questionnaire(models.Model):    
    title = models.CharField("Название опросника", max_length=25,  null=True, blank=True)
    description = models.CharField("Описание", max_length=256, null=True, blank=True)
    questions = models.ManyToManyField(
        Question, 
        verbose_name="Вопросы в текущем опроснике", 
        related_name="questionnaires" 
        )
    users = models.ManyToManyField(
        Employee,
        through="AppointTo", 
        related_name="user", 
        verbose_name="Открытые для отрудников", 
        blank=True)
    
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "опросник"
        verbose_name_plural = '№3: сформировать опросник'


class EmployeeAnswer(models.Model):
    users = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE, verbose_name='сотрудники')
    questionnaires = models.ForeignKey(Questionnaire,  null=True, blank=True, on_delete=models.CASCADE, verbose_name='опросник')
    questions = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='employee_answers', verbose_name='вопрос')
    user_answer = models.CharField("Ответ", max_length=256,  null=True, )
    is_correct = models.BooleanField(default=False, verbose_name='верно')
    
    def __str__(self):
        if self.users.user_name.username:
            return self.users.user_name.username

    class Meta:
        verbose_name = "ответы сотрудников" 
        verbose_name_plural = '№5: посмотреть ответы сотрудников'     


class AppointTo(models.Model):
    users = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        blank=True,
        verbose_name='сотрудник' )
    questionnaires = models.ForeignKey(
        Questionnaire, 
        on_delete=models.CASCADE, 
        blank=True,
        related_name="appoint",  
        verbose_name='опросник' )
    date_start = models.DateField("Дата начала опроса", default=datetime.now, blank=True)
    date_finish = models.DateField("Дата окончания опроса", default=datetime.now, blank=True)
 
    @property
    def isOpen(self):
        # finish = AppointTo.objects.filter(date_finish__gt=datetime.today().date(), questionnaires_id=self.id)
        # for xxx in finish:
        #     print(xxx.date_finish) 
        if self.date_finish >= datetime.today().date(): 
            return True
        else:
            return False
        
    def __srt__(self):
        if self.users.user_name.username:
            return  self.users.user_name.username

    class Meta:
        verbose_name = ' опросник  сотруднику '
        verbose_name_plural = '№4: назначить опросник'  


# class ShowResults(models.Model):



# class RightAnswer(models.Model):
#     question = models.ForeignKey(Question, null=True, related_name='good_answer', on_delete=models.CASCADE)
#     answer = models.CharField(max_length=128, null=True)
    
#     class Meta:
#         verbose_name = "Правильныйтвет"
#         verbose_name_plural = 'Правильные ответы'
        


# class QuestionnaireContent(models.Model):
#     question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE, verbose_name="Вопрос")
#     questionnaire = models.ForeignKey(Questionnaire, null=True,
#      on_delete=models.CASCADE, verbose_name="Опросник")
#     time_to_answer = models.SmallIntegerField("Время на ответ", default=0)
#     answer_weight = models.SmallIntegerField("Вес ответа", default=1)

#     def __str__(self):
#         return f"{self.questionnaire} - {self.question} - {self.time_to_answer} - {self.answer_weight}"

#     class Meta:
#         verbose_name = "Содержимое опросника"
#         verbose_name_plural = "Содержимое опросников"

   

# class QuestionnaireResult(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Сотрудник")
#     questionnaire_content = models.ForeignKey(QuestionnaireContent, on_delete=models.CASCADE)
#     answer = JSONField(default=list) # список правильных ответов по всему опроснику

#     @property
#     def score(self):
#         question = self.questionnaire_content.question
#         weight = self.questionnaire_content.answer_weight
#         answerList = []
#         if not isinstance (self.answer, list):
#             answerList.append(self.answer)
#         else:
#             answerList = self.answer
#         response = EmployeeAnswer.objects.filter(question=question)
#         answer_score = 0
#         for i in response:
#             if self.questionnaire_content.question.question_type == 'CHECKBOXES':
#                 for j in answerList:
#                     if i.user_answer == j:
#                         answer_score += weight
#             if self.questionnaire_content.question.question_type == 'RADIO':
#                 for j in answerList:
#                     if i.user_answer == j:
#                         if i.isCorrect:
#                             answer_score += 1
#                         # else:
#                         #     answer_score -= 1
#         return answer_score 
#         # * self.questionnaire_content.answer_weight

#     class Meta:
#         verbose_name = "Результат по опроснику"
#         verbose_name_plural = "Результаты по всем опросникам"