document.addEventListener('DOMContentLoaded', function () {
    document.body.style.opacity = 1;
});

document.addEventListener('click', function (e) {
    const target = e.target;

    // Проверяем, что это ссылка, ведущая на другую страницу
    if (target.tagName === 'A' && target.getAttribute('href').startsWith('/')) {
        e.preventDefault();

        // Затухание страницы перед переходом
        document.body.style.opacity = 0;

        // Задержка перед фактическим переходом
        setTimeout(function () {
            window.location.href = target.getAttribute('href');
        }, 500); // Время анимации в миллисекундах (здесь 0.5 секунды)
    }
});