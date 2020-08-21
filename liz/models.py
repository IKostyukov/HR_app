from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
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
    

    def __str__(self):
        return self.question 
    
    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = '№2: вопросы'


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


class Answer(models.Model):
    questions = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='вопросы')
    questionnaires = models.ForeignKey(Questionnaire,  null=True, blank=True, on_delete=models.CASCADE, related_name='answer_in_questionnaire', verbose_name='опросник')
    variant = models.CharField("варианты ответа в опроснике", max_length=128,  null=True)
    is_right_variant = models.BooleanField("укажите правильный ли это вариант?")
    answer_weight = models.SmallIntegerField("баллы", default=0)
    time_for_answer = models.PositiveSmallIntegerField("время на ответ, сек.", default=15)
    def __str__(self):
        return self.variant 
    
    class Meta:
        verbose_name = "вариант для ответа"
        verbose_name_plural = "№6: варианты для ответов"

    def get_rightlist(request):
        question_id = request.POST["question_id"]
        right_variants = []
        variants = Answer.objects.filter(questions_id=question_id).filter(is_right_variant=True)
        for ok in variants:
            right_variants.append(ok.variant)
        return right_variants

    def ditails_qestionnaire(questionnaire_id, right_id):
        quests = Question.objects.filter(questionnaires__id=questionnaire_id)  
        employee_answers = EmployeeAnswer.objects.filter(users_id = right_id, questionnaires_id = questionnaire_id)
        variants = Answer.objects.filter(questions__questionnaires__users = right_id, questions__questionnaires__id = questionnaire_id)
        weight_questionnaire = 0
        list_answered = [] 
        for quest in quests:
            for employee_answer in employee_answers:
                if employee_answer.questions_id == quest.id and employee_answer.questions_id not in  list_answered:
                    list_answered.append(employee_answer.questions_id)  
                if  employee_answer.questions_id == quest.id and employee_answer.is_correct and employee_answer.in_time:
                    for variant in variants:
                        if variant.questions_id == quest.id and variant.variant == employee_answer.user_answer:
                            weight_questionnaire += variant.answer_weight               
        dict_questionnaire = {
            "weight_questionnaire":weight_questionnaire,
            "employee_answers":employee_answers,
            "quests":quests,
            "variants":variants,
            "list_answered":list_answered,
            }
        return dict_questionnaire  
    

class EmployeeAnswer(models.Model):
    users = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE,related_name='users', verbose_name='сотрудники')
    questionnaires = models.ForeignKey(Questionnaire,  null=True, blank=True, on_delete=models.CASCADE, related_name='employee_questionnaire', verbose_name='опросник')
    questions = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='employee_question', verbose_name='вопрос')
    user_answer = models.CharField("Ответ", max_length=256,  null=True, )
    is_correct = models.BooleanField(default=False, verbose_name='верно')
    in_time = models.BooleanField(default=True, verbose_name='вовремя')
    
    class Meta:
        verbose_name = "ответы сотрудников" 
        verbose_name_plural = '№5: посмотреть ответы сотрудников'     


    def __str__(self):
        if self.users.user_name.username:
            return self.users.user_name.username


    def create_instans(self, request, answer):
        user_name =  Employee.objects.get(user_name=request.user)
        question_id = request.POST.get("question_id")
        questionnaire_id = request.POST.get("questionnaire_id")
        employee_answer = EmployeeAnswer(
                        users=user_name, 
                        questions_id=question_id,
                        questionnaires_id=questionnaire_id, 
                        user_answer=answer)
        return employee_answer

    def check_time(request):
        format = '%Y-%m-%d %H:%M:%S.%f'
        time_finish = datetime.strptime(str(datetime.now()), format) 
        time_start_str = request.POST['time_start']
        time_start = datetime.strptime(time_start_str, format)
        time_for_answer = request.POST['time_for_answer']
        delta_real = time_finish - time_start
        delta_prompt = timedelta(seconds=int(time_for_answer))
        if delta_real < delta_prompt: 
            return True
        else:
            return False

    def save_answer(request, answer, right_variants, time_ok):
        instans = EmployeeAnswer()
        employee_answer = instans.create_instans(request, answer)
        if answer in right_variants:
            employee_answer.is_correct = True
        if time_ok:
            employee_answer.save()
            return
        else:
            employee_answer.in_time = False
            employee_answer.save()
            return              


    @property
    def answer_weight_func(self):
        """ Этот атрибут выводит набранные баллы пользователя за отдельный ответ
         в админке №5 "Посмотреть ответы сотрудников" (столбец"points")""" 
        questionnaire_id = self.questionnaires.id
        user_id = self.users.user_name_id
        question_id = self.questions.id
        # quests = Question.objects.filter(questionnaires__id=questionnaire_id)  
        # employee_answers = EmployeeAnswer.objects.filter(users__user_name_id = user_id, questionnaires_id = questionnaire_id)
        variants = Answer.objects.filter(questions__questionnaires__users__user_name_id=user_id, questions__questionnaires__id = questionnaire_id)  
        # for quest in quests:
        #     if  self.questions_id == quest.id:
        for variant in variants:
            if variant.questions_id == question_id and variant.variant == self.user_answer:
                return variant.answer_weight      

    # @property    #!!! СИЛЬНО ТОРМОЗИТ ЗАГРУЗКУ СТРАНИЦЫ ПАНЕЛИ АДМИНИСТРАТОРА
    #                #!!! посткольку для каждого ответа на каждый вопрос каждого пользователя запускает эту функцию.
    #                # !!! Значение тотал ограничиваю подсчетом функции total_weight на стр №4 админки 
    # def total_weight_func(self):  
    #     #  """Этот атрибут выводит набранные баллы пользователя за пройденный опросник
    #     #  в админке №5 "Посмотреть ответы сотрудников" (столбец"total")""" 
    #     questionnaire_id = self.questionnaires.id
    #     user_id = self.users.user_name_id
    #     quests = Question.objects.filter(questionnaires__id=questionnaire_id)  
    #     employee_answers = EmployeeAnswer.objects.filter(users__user_name_id = user_id, questionnaires_id = questionnaire_id)
    #     variants = Answer.objects.filter(questions__questionnaires__users__user_name_id=user_id, questions__questionnaires__id = questionnaire_id)  
    #     weight_questionnaire = 0
    #     for quest in quests:
    #         for employee_answer in employee_answers:
    #             if  employee_answer.questions_id == quest.id and employee_answer.is_correct:
    #                 for variant in variants:
    #                     if variant.questions_id == quest.id and variant.variant == employee_answer.user_answer:
    #                         weight_questionnaire += variant.answer_weight             
    #     return weight_questionnaire


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

    class Meta:
        verbose_name = ' опросник  сотруднику '
        verbose_name_plural = '№4: назначить опросник или посмотреть общие баллы'  


 
    @property
    def isOpen(self):
        # finish = AppointTo.objects.filter(date_finish__gt=datetime.today().date(), questionnaires_id=self.id)
        # for xxx in finish:
        #     print(xxx.date_finish) 
        if self.date_finish >= datetime.today().date(): 
            return True
        else:
            return False

    @property
    def total_weight(self):
        """Атрибут выводит набранные баллы пользователя за пройденный опросник
         в панель администратора в "Назначить опросник" колонка 'total' """
        questionnaire_id = self.questionnaires.id
        user_id = self.users.user_name_id
        quests = Question.objects.filter(questionnaires__id=questionnaire_id)  
        employee_answers = EmployeeAnswer.objects.filter(users__user_name_id = user_id, questionnaires_id = questionnaire_id)
        variants = Answer.objects.filter(questions__questionnaires__users__user_name_id=user_id, questions__questionnaires__id = questionnaire_id)
        weight_questionnaire = 0
        for quest in quests:
            for employee_answer in employee_answers:
                if  employee_answer.questions_id == quest.id and employee_answer.is_correct and employee_answer.in_time:
                    for variant in variants:
                        if variant.questions_id == quest.id and variant.variant == employee_answer.user_answer:
                            weight_questionnaire += variant.answer_weight             
        return weight_questionnaire
        
    def __srt__(self):
        if self.users.user_name.username:
            return  self.users.user_name.username

    




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