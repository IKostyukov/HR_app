from django.db import models
from django.contrib.auth.models import User

# Create your models here.

USER_TYPE = [
        ('MG', 'Manager'),
        ('CW', 'Coworker'), 
        ]

class Employee(models.Model):
    MANAGER = 'MG'
    COWORKER = 'CW'    
    
    user_type = models.CharField(
        max_length=10, 
        choices = USER_TYPE, 
        default = COWORKER,
        null=True, blank=True)

    user_name = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name='employee')
    department =  models.CharField(max_length=100)

    def __str__(self):
        return self.user_name.username

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"



class Question(models.Model):
    question = models.TextField()
    image = models.ImageField(upload_to='photos/%Y/%m/%d', null=True, blank=True)
    QUESTIONE_TYPE = [
        ('RADIO',  'c одним вариантом ответа'),
        ('CHECKBOXES', ' с несколькими вариантами'),
    ]
    question_type = models.CharField(max_length=10, verbose_name='тип вопросов',
     choices=(QUESTIONE_TYPE), blank=True)
    point = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.question 
    
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = 'Вопросы'


# class QuestionnaireType(models.Model):
    
#     qr_title = models.CharField(max_length=25, verbose_name='Название опросника')
#     qr_description = models.TextField(verbose_name='Описание')
    
#     def __str__(self):
#         return self.qr_title

#     class Meta:
#         verbose_name = "Опросник"
#         verbose_name_plural = 'Опросники'
    
    

class QuestionnaireContent(models.Model):    
    title = models.CharField(max_length=25,  null=True, blank=True,  verbose_name='Название опросника')
    description = models.CharField(max_length=256, null=True, blank=True,  verbose_name='Описание')
    question = models.ManyToManyField(Question)
    # questionnarie = models.ForeignKey(QuestionnaireType,  on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Содержание опросника"
        verbose_name_plural = 'Содержание опросников'

class RightAnswer(models.Model):
    right_answer = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Правильныйтвет"
        verbose_name_plural = 'Правильные ответы'
    

class EmployeeAnswer(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='user')
    question = models.ForeignKey(QuestionnaireContent, on_delete=models.CASCADE, related_name='answered_question')
    user_answer = models.CharField( null=True, blank=True,  max_length=256)
    correct = models.BooleanField()

    def __str__(self):
        return str(self.user.user_name.username)
    
    class Meta:
        verbose_name = "ответ сотрудника"
        verbose_name_plural = 'ответы сотрудников'





