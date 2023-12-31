# CreditAPI
## Опис проекту

Цей проект є API-сервісом для створення та зміни графіка платежів по кредиту. Сервіс розроблено з використанням Django та Django REST Framework, а база даних SQLite використовується для зберігання даних.

## Встановлення

Для запуску цього проекту вам знадобляться Docker та Docker Compose. Встановіть їх, дотримуючись офіційних інструкцій для вашої операційної системи.

1. Склонуйте репозиторій проекту:

   ```bash
   git clone https://github.com/DanilenkoDanil/CreditAPI.git
   cd CreditAPI
   ```

2. Запустіть Docker Compose для збирання та запуску контейнерів:

   ```bash
   docker-compose up
   ```

   Docker-контейнери будуть створені та запущені. Ви побачите вивід, включаючи інформацію про запуск вашого Django-додатку.

3. Виконайте міграції:

   ```bash
   docker-compose run --rm app python manage.py migrate
   ```
   
4. Ваш API-сервіс буде доступний за адресою `http://localhost:8000`. Ви можете надсилати запити до вашого API та використовувати його як звичайно.

## Використання

Ви можете використовувати будь-який інструмент для надсилання HTTP-запитів (наприклад, curl або Postman), щоб взаємодіяти з API-сервісом. Нижче наведені приклади використання кількох ендпоінтів:

1. Створення графіка платежів:
   - URL: `http://localhost:8000/api/create-payment-schedule/`
   - Метод: POST
   - Тіло запиту (JSON):
     ```json
     {
       "amount": 1000,
       "loan_start_date": "2024-10-01",
       "number_of_payments": 4,
       "periodicity": 1,
       "interest_rate": 0.1
     }
     ````
   Примітка: В параметрі periodicity зазначено pk запису відповідного об'єкту. Готові варіанти можна переглянути у адмінці за посиланням http://localhost:8000/admin/ (admin:admin).

2. Зміна суми тіла платежу:
   - URL: `http://localhost:8000/api/reduce-principal/{credit_id}/{payment_id}/`
   - Метод: PATCH
   - Тіло запиту (JSON):
     ```json
     {
       "amount": 50
     }
     ```
   Замініть `{credit_id}` та `{payment_id}` на відповідні ідентифікатори кредиту та платежу.

## Тестування

Для запуску тестів Django введіть наступну команду в командному рядку:

```bash
docker-compose run --rm app python manage.py test
```

Це запустить тести та виведе результати в командному рядку.

## Висновок

Тепер у вас є готовий API-сервіс для створення та зміни графіка платежів по кредиту. Ви можете використовувати його для управління платежами та проведення розрахунків. Вільно налаштовуйте та розширюйте функціональність API відповідно до ваших потреб.
