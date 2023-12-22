from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Question, Choice, TestResult
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
import base64
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages


def home(request):
    return render(request, 'base.html')
def test(request):
    if request.method == 'POST':
        score = 0
        for question in Question.objects.all():
            user_choice_id = request.POST.get(f'question_{question.id}')
            if user_choice_id:
                user_choice = Choice.objects.get(id=user_choice_id)
                score += user_choice.points

        result_message = get_result_message(score)

        # Если пользователь не авторизован, предложить сохранить результаты
        if not request.user.is_authenticated:
            request.session['test_result'] = {'score': score, 'result_message': result_message}
            return render(request, 'BeckTest/offer_save_result.html', {'score': score, 'result_message': result_message})

        # Если пользователь авторизован, сохраняем результаты в базе данных
        TestResult.objects.create(user=request.user, score=score, result_message=result_message)

        # Вместо вызова функции test_results, возвращаем рендеринг страницы с результатами
        return render(request, 'BeckTest/test_results.html', {'score': score, 'result_message': result_message})

    questions = Question.objects.all()
    return render(request, 'BeckTest/test.html', {'questions': questions})


@login_required
def offer_save_result(request):
    if request.method == 'POST':
        save_result_choice = request.POST.get('save_result_choice')

        if save_result_choice == 'yes':
            # Если пользователь соглашается сохранить результат, перенаправляем на страницу регистрации или входа
            return redirect('registration_or_login')
        elif save_result_choice == 'no':
            # Если пользователь отказывается, перенаправляем на главную страницу
            return redirect('test')  # Замените 'home' на ваш URL-путь к главной странице
        elif save_result_choice == 'send_email':
            # Если пользователь хочет отправить результаты на электронную почту, перенаправляем на страницу ввода адреса
            return redirect('enter_email')

    return render(request, 'BeckTest/offer_save_result.html')


def test_results(request, score):
    # Сохраняем результат в сессии
    request.session['test_score'] = score
    return render(request, 'BeckTest/test_results.html', {'score': score})

def get_result_message(score):
    if score <= 9:
        return "Отсутствие депрессивных симптомов."
    elif 10 <= score <= 18:
        return "Легкая депрессия, астено-субдепрессивная симптоматика, м.б. у соматических больных или невротический уровень."
    elif 19 <= score <= 29:
        return "Умеренная депрессия, критический уровень."
    elif 30 <= score <= 63:
        return "Явно выраженная депрессивная симптоматика, не исключена эндогенность."
    else:
        return "Некорректные баллы для оценки."

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if 'test_result' in request.session:
                test_result_data = request.session['test_result']
                TestResult.objects.create(user=user, score=test_result_data['score'], result_message=test_result_data['result_message'])
                del request.session['test_result']
            return redirect('home')
        else:
            # Выводим сообщения об ошибках
            error_messages = {
                'username': 'Поле "Имя пользователя" содержит ошибку',
                'first_name': 'Поле "Имя" содержит ошибку',
                'second_name': 'Поле "Фамилия" содержит ошибку',
                'middle_name': 'Поле "Отчество" содержит ошибку',
                'date_of_birth': 'Поле "Дата рождения" содержит ошибку',
                'email': 'Поле "Email" содержит ошибку',
                'phone_number': 'Поле "Номер телефона" содержит ошибку',
                'password1': 'Поле "Пароль" содержит ошибку',
                'password2': 'Поле "Подтверждение пароля" содержит ошибку.',
            }

            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error_messages.get(field, field.capitalize())}: {error}")

    else:
        form = CustomUserCreationForm()

    return render(request, 'BeckTest/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if 'test_result' in request.session:
                    quiz_result_data = request.session['test_result']
                    TestResult.objects.create(user=user, score=quiz_result_data['score'], result_message=quiz_result_data['result_message'])
                    del request.session['test_result']
                return redirect('home')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль. Попробуйте снова.')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль. Попробуйте снова.')
    else:
        form = AuthenticationForm()
    return render(request, 'BeckTest/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def view_results(request):
    user_results = TestResult.objects.filter(user=request.user)
    return render(request, 'BeckTest/view_results.html', {'user_results': user_results})

def registration_or_login(request):
    return render(request, 'BeckTest/registration_or_login.html')

def view_results(request):
    # Получаем результаты теста для текущего пользователя
    test_results = TestResult.objects.filter(user=request.user).order_by('date_completed')

    # Получаем данные для построения графика
    dates = [result.date_completed.strftime('%d-%m-%Y') if result.date_completed else 'N/A' for result in test_results]
    scores = [result.score for result in test_results]

    # Строим линейный график
    plt.plot(dates, scores, marker='o')
    plt.title('Результаты теста по датам')
    plt.xlabel('Дата прохождения')
    plt.ylabel('Баллы')

    # Добавляем метки с датами
    for i, date in enumerate(dates):
        plt.text(date, scores[i], date, fontsize=8, ha='right', va='bottom')

    # Сохраняем график в байтовом объекте
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Кодируем изображение в base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    # Отправляем изображение и результаты в шаблон
    return render(request, 'BeckTest/view_results.html',
                  {'test_results': test_results, 'image_base64': image_base64})

def enter_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            try:
                send_email(email, request.user, request.session['test_result']['score'], request.session['test_result']['result_message'])
                del request.session['test_result']
                return render(request, 'BeckTest/email_sent.html')  # Создайте шаблон email_sent.html с сообщением об успешной отправке
            except Exception as e:
                print(e)  # Выводим ошибку в консоль для отладки
                return render(request, 'BeckTest/email_error.html')  # Создайте шаблон email_error.html с сообщением об ошибке отправки

    return render(request, 'BeckTest/enter_email.html')

def send_email(email, user, score, result_message):
    subject = 'Результаты теста'
    message = f'Ваш результат: {score}\nСообщение: {result_message}'
    html_message = render_to_string('BeckTest/email_templates.html', {'user': user, 'score': score, 'result_message': result_message})
    plain_message = strip_tags(html_message)
    from_email = 'wolfexe@yandex.ru'
    recipient_list = [email]

    # Отправляем электронное письмо
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
