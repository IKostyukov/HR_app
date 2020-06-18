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

    # class Meta:
    #     user_name = "Сотрудник"




class Question(models.Model):
    question = models.TextField()
    image = models.ImageField(upload_to='photos/%Y/%m/%d', null=True, blank=True)
    
    def __str__(self):
        return self.question 


class QuestionnaireType(models.Model):
    QUESTIONNARIE_TYPE = [
        ('RADIO',  'один вариант ответа'),
        ('CHECKBOXES', 'несколько вариантов'),
    ]
    qr_type = models.CharField(max_length=10, verbose_name='тип вопросов',
     choices=(QUESTIONNARIE_TYPE), blank=True)
    qr_title = models.CharField(max_length=25, verbose_name='Название опросника')
    qr_description = models.TextField(verbose_name='Описание')
    
    def __str__(self):
        return self.qr_title
    
    

class QuestionnaireContent(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    questionnarie = models.ForeignKey(QuestionnaireType,  on_delete=models.CASCADE)
    point = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.questionnarie.qr_title


class RightAnswer(models.Model):
    right_answer = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    

class EmployeeAnswer(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='user')
    question = models.ForeignKey(QuestionnaireContent, on_delete=models.CASCADE, related_name='answered_question')
    user_answer = models.ManyToManyField(QuestionnaireContent)
    correct = models.BooleanField()

    def __str__(self):
        return self.user.user_name.username





