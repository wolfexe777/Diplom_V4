from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Question, Choice, CustomUser, TestResult

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    actions_on_top = False
    inlines = [ChoiceInline]
    actions = ['delete_with_choices']

    def delete_with_choices(self, request, queryset):
        for question in queryset:
            # Здесь вы должны добавить код удаления связанных ответов на вопросы
            question.delete()

    delete_with_choices.short_description = "Удалить с ответами"

admin.site.register(Question, QuestionAdmin)

class TestResultInline(admin.TabularInline):
    model = TestResult
    extra = 0
    fields = ('score', 'result_message', 'date_completed')
    readonly_fields = ('score', 'result_message', 'date_completed')

class CustomUserAdmin(UserAdmin):
    actions_on_top = False
    list_display = (
        'username', 'email', 'first_name', 'second_name', 'middle_name','date_of_birth',
        'phone_number', 'score', 'result_message', 'date_completed'
    )
    search_fields = ('username', 'email', 'first_name', 'second_name', 'phone_number')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'first_name', 'second_name', 'middle_name', 'phone_number','date_of_birth')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    inlines = [TestResultInline]

    def score(self, obj):
        return obj.test_results.first().score if obj.test_results.first() else ''

    def result_message(self, obj):
        return obj.test_results.first().result_message if obj.test_results.first() else ''

    def date_completed(self, obj):
        return obj.test_results.first().date_completed if obj.test_results.first() else ''

    score.admin_order_field = 'test_results__score'
    result_message.admin_order_field = 'test_results__result_message'
    date_completed.admin_order_field = 'test_results__date_completed'

    score.short_description = 'Баллы теста'
    result_message.short_description = 'Результаты теста'
    date_completed.short_description = 'Дата прохождения теста'


    actions = ['delete_with_results']


    def delete_with_results(self, request, queryset):
        for user in queryset:
            user.delete()

    delete_with_results.short_description = "Удалить с результатами тестов"

admin.site.register(CustomUser, CustomUserAdmin)


class TestResultAdmin(admin.ModelAdmin):
    list_display = ('display_username', 'display_score', 'display_result_message', 'display_date_completed')
    search_fields = ('user__username', 'score', 'date_completed')

    def display_username(self, obj):
        return obj.user.username

    def display_score(self, obj):
        return obj.score

    def display_result_message(self, obj):
        return obj.result_message

    def display_date_completed(self, obj):
        return obj.date_completed

    display_username.short_description = 'Ник клиента'
    display_score.short_description = 'Баллы теста'
    display_result_message.short_description = 'Сообщение о результате теста'
    display_date_completed.short_description = 'Дата прохождения теста'

admin.site.register(TestResult, TestResultAdmin)