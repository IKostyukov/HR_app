# hr_app
Application for conducting online surveys of employees or students based on PostgreSQL. The application is deployed on the Heroku server at https://vast-waters-63560.herokuapp.com/
The user to whom the superuser (administrator) assigns manager rights can manage the entire process through the admin panel at https://vast-waters-63560.herokuapp.com/admin
In the admin panel, the manager can:
1) Work with any registered user
2) Create questions
- attach the necessary pictures to them
- and also give four options for an answer to each question
- rate each answer option with a certain number of points (default 0)
- set response time for this question (default 15 seconds)
3) Create questionnaires
- create a questionnaire from any combination of questions
4) Assign any questionnaire or see total scores
- filters are available # by date # by user  # by questionnaire
- the manager can assign any selected questionnaire to any registered user
- select the start and end date of access to this questionnaire for the selected user
- after the user completes the questionnaire, the Total column displays all the points scored by the user in this questionnaire (points are counted only for the correct answer and if the user meets the time)
5) View user responses
- filters are available # by users  # by questionnaires
- you can see all the results: what answer the user gave
- is the answer correct
- whether the user met the time
- how many points was the answer

Приложение для проведения онлайн-опросов сотрудников или студентов на базе PostgreSQL. Приложение развернуто на сервере Heroku по адресу https://vast-waters-63560.herokuapp.com/
Пользователь, которому суперпользователь (администратор) назначает права администратора, может управлять всем процессом через админку по адресу https://vast-waters-63560.herokuapp.com/admin
В админке менеджер может:
1) Работать с любым зарегистрированным пользователем
2) Создавать вопросы
- прикрепить к ним нужные картинки
- а также дать четыре варианта ответа на каждый вопрос
- оцените каждый вариант ответа определенным количеством баллов (по умолчанию 0)
- установить время ответа на этот вопрос (по умолчанию 15 секунд)
3) Создавать анкеты
- создать анкету из любой комбинации вопросов
4) Назначить анкету или посмотреть общие баллы
- фильтры доступны # по дате # по пользователю # по анкете
- менеджер может назначить любую выбранную анкету любому зарегистрированному пользователю
- выберите дату начала и окончания доступа к этой анкете для выбранного пользователя
- после того, как пользователь заполнил анкету, в столбце Total отображаются все баллы, набранные пользователем в этой анкете (баллы засчитываются только за правильный ответ и если пользователь уложился во время)
5) Просмотреть ответы пользователей
- фильтры доступны # по пользователям # по анкетам
- можно увидеть все результаты: какой ответ дал пользователь
- правильный ответ
- уложился ли пользователь в срок
- сколько баллов был ответ
