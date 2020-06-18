# class User():
#     type = Choices() #Manage|Cowoker

# class Question():
#     title = Text() Сколько будет 2+2?
#     image = Image()

# class Answer():
#     title = Char() #4 # answer
#     question = Question() 
#     correct = Boolean() # True

# class QuestionList():
#     type = Choices() #Опросник|Тест
#     title = Char() # Математический тест
#     description = Text() #....

# class QuestionInList():
#     question = Question()
#     question_list = QuestionList()
#     weight = Integer() #Вес вопроса в опроснике

# class userAnswer():
#     user = User():
#     question_in_list = QuestionInList()
#     anwers = ManyToMany()

# Дано
# user = User(id=1)
# question = Question(id=1)
# Найти 
# в question_in_list
# question: получить сумму всех весов этого юзера по всем опросникам
# Решение
# UserAnswer.filter(user=user, question_in_list__question=question)

question_list = QuestionList(id=1)
question_in_list = QuestionInList.filter(question_list=question_list)

# {% for question_in_list in question_in_list %}
#     title: question_in_list.question.title
#     for answer in question_in_list.question.answers:
#         answer.title
# {% endfor %}



