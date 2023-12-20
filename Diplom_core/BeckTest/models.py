from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255, verbose_name='Имя', blank=True, null=True)
    second_name = models.CharField(max_length=255, verbose_name='Фамилия', blank=True, null=True)
    middle_name = models.CharField(max_length=255, verbose_name='Отчество', blank=True, null=True)
    email = models.EmailField(unique=True, null=False, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, verbose_name='Номер телефона')
    groups = models.ManyToManyField(Group, related_name='custom_users', blank=True, verbose_name='Группы')
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_users', blank=True, verbose_name='Права пользователя'
    )
    def __str__(self):
        return self.username

class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='Вопрос', null=True, blank=True)

    def __str__(self):
        return self.question_text

    class Meta:
        ordering = ['id']
        verbose_name = 'Вопрос теста'
        verbose_name_plural = 'Вопросы теста'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    choice_text = models.CharField(max_length=200, null=True, verbose_name='Варианты ответов')
    points = models.IntegerField(default=0, verbose_name='Баллы')

    def __str__(self):
        return self.choice_text

class TestResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='test_results',  null=True, blank=True)
    score = models.IntegerField()
    result_message = models.CharField(max_length=255, null=True, blank=True)
    date_completed = models.DateTimeField(auto_now_add=True, null=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"Результат {self.user.username}"

    class Meta:
        verbose_name = 'Результат клиета'
        verbose_name_plural = 'Результаты клиентов'
