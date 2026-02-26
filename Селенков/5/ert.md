Ниже код с нумерацией функций и подробными пояснениями по каждой строке. Источники пометил в конце ответа. [habr](https://habr.com/ru/companies/bft/articles/777348/)

***

## Код с номерами функций

```python
import psycopg2
from datetime import date

DB_CONFIG = {
    'host': 'localhost',
    'database': '21is5',
    'user': 'postgres',
    'password': '1111',
    'port': '5432'
}

def connect():  # Функция 0
    return psycopg2.connect(**DB_CONFIG)

def add_workout(ex, d, sets, reps, w, diff, notes):  # Функция 1
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO training_logs
           (exercise_name, training_date, sets, reps,
            weight_kg, difficulty, notes)
           VALUES (%s,%s,%s,%s,%s,%s,%s)
           RETURNING id""",
        (ex, d, sets, reps, w, diff, notes)
    )
    wid = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    print("Добавлено, ID =", wid)

def show_all():  # Функция 2
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, exercise_name, training_date, sets, reps, "
        "weight_kg, difficulty, notes "
        "FROM training_logs ORDER BY training_date DESC"
    )
    for r in cur.fetchall():
        print(*r, sep=" | ")
    cur.close()
    conn.close()

def search_ex(name):  # Функция 3
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        """SELECT id, exercise_name, training_date, sets, reps,
                  weight_kg, difficulty, notes
           FROM training_logs
           WHERE lower(exercise_name) LIKE lower(%s)
           ORDER BY training_date DESC""",
        (f"%{name}%",)
    )
    for r in cur.fetchall():
        print(*r, sep=" | ")
    cur.close()
    conn.close()

def filter_date(d1, d2):  # Функция 4
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        """SELECT id, exercise_name, training_date, sets, reps,
                  weight_kg, difficulty, notes
           FROM training_logs
           WHERE training_date BETWEEN %s AND %s
           ORDER BY training_date""",
        (d1, d2)
    )
    for r in cur.fetchall():
        print(*r, sep=" | ")
    cur.close()
    conn.close()

def update_workout(wid, w, notes):  # Функция 5
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE training_logs SET weight_kg=%s, notes=%s WHERE id=%s",
        (w, notes, wid)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Обновлено")

def delete_workout(wid):  # Функция 6
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM training_logs WHERE id=%s", (wid,))
    conn.commit()
    cur.close()
    conn.close()
    print("Удалено")

def stats():  # Функция 7
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        """SELECT count(*), max(weight_kg),
                  avg(weight_kg), avg(reps)
           FROM training_logs"""
    )
    total, mx, avg_w, avg_r = cur.fetchone()
    cur.close()
    conn.close()
    print("Всего записей:", total)
    print("Макс. вес:", mx)
    print("Средний вес:", round(avg_w or 0, 2))
    print("Средние повторы:", round(avg_r or 0, 2))

def main():  # Функция 8
    while True:
        print("\n1 Добавить"
              "\n2 Показать все"
              "\n3 Поиск по упражнению"
              "\n4 Фильтр по дате"
              "\n5 Обновить запись"
              "\n6 Удалить запись"
              "\n7 Статистика"
              "\n0 Выход")
        cmd = input("Выбор: ")

        if cmd == "1":
            ex = input("Упражнение: ")
            d = input("Дата YYYY-MM-DD (Enter = сегодня): ") or str(date.today())
            sets = int(input("Подходы: "))
            reps = int(input("Повторы: "))
            w = float(input("Вес: "))
            diff = input("Сложность (легко/нормально/тяжело): ")
            notes = input("Заметки: ")
            add_workout(ex, d, sets, reps, w, diff, notes)

        elif cmd == "2":
            show_all()

        elif cmd == "3":
            search_ex(input("Название упражнения: "))

        elif cmd == "4":
            d1 = input("С даты YYYY-MM-DD: ")
            d2 = input("По дату YYYY-MM-DD: ")
            filter_date(d1, d2)

        elif cmd == "5":
            wid = int(input("ID: "))
            w = float(input("Новый вес: "))
            notes = input("Новые заметки: ")
            update_workout(wid, w, notes)

        elif cmd == "6":
            delete_workout(int(input("ID: ")))

        elif cmd == "7":
            stats()

        elif cmd == "0":
            break

        else:
            print("Нет такого пункта")

if __name__ == "__main__":
    main()
```

***

## Пояснение по строкам и словам

### Импорт и конфиг

- `import psycopg2` — подключаем библиотеку для работы с PostgreSQL из Python. [eax](https://eax.me/2019/2019-11-05-python-psycopg2.html)
- `from datetime import date` — берём класс `date`, чтобы получать сегодняшнюю дату. [pythonlib](https://pythonlib.ru/library-theme53)

```python
DB_CONFIG = {
    'host': 'localhost',
    'database': '21is5',
    'user': 'postgres',
    'password': '1111',
    'port': '5432'
}
```

- `DB_CONFIG` — словарь с настройками подключения.  
- `'host': 'localhost'` — сервер базы данных, здесь тот же компьютер.  
- `'database': '21is5'` — имя базы, которую ты создал.  
- `'user': 'postgres'` — пользователь PostgreSQL.  
- `'password': '1111'` — пароль пользователя.  
- `'port': '5432'` — порт, на котором работает PostgreSQL (стандартный 5432). [wiki.postgresql](https://wiki.postgresql.org/wiki/Psycopg2_Tutorial)

***

### Функция 0: `connect`

```python
def connect():
    return psycopg2.connect(**DB_CONFIG)
```

- `def connect():` — объявление функции без аргументов.  
- `psycopg2.connect(...)` — создаёт соединение с базой. [eax](https://eax.me/2019/2019-11-05-python-psycopg2.html)
- `**DB_CONFIG` — распаковывает словарь как named‑аргументы (`host=.., database=..`).  
- `return` — возвращает объект соединения, чтобы другие функции могли его использовать.  

***

### Функция 1: `add_workout`

```python
def add_workout(ex, d, sets, reps, w, diff, notes):
```

- Аргументы: название упражнения, дата, подходы, повторы, вес, сложность, заметки — всё по ТЗ.

```python
    conn = connect()
```

- `conn` — объект соединения с базой, полученный из функции 0.

```python
    cur = conn.cursor()
```

- `cursor()` — создаёт курсор, через него выполняются SQL‑запросы. [psycopg](https://www.psycopg.org/docs/cursor.html)

```python
    cur.execute(
        """INSERT INTO training_logs
           (exercise_name, training_date, sets, reps,
            weight_kg, difficulty, notes)
           VALUES (%s,%s,%s,%s,%s,%s,%s)
           RETURNING id""",
        (ex, d, sets, reps, w, diff, notes)
    )
```

- `cur.execute` — выполняет SQL‑команду.  
- Тройные кавычки `"""..."""` — многострочная строка с запросом.  
- `INSERT INTO training_logs (...) VALUES (...)` — вставка новой строки в таблицу.  
- `%s` — параметр запроса (подставится безопасно через psycopg2, защита от SQL‑инъекций). [pythonlib](https://pythonlib.ru/library-theme53)
- `RETURNING id` — после вставки вернуть значение поля `id`.  
- Второй аргумент `(... )` — кортеж значений, которые подставятся на места `%s`.

```python
    wid = cur.fetchone()[0]
```

- `fetchone()` — берёт одну строку результата (там лежит только поле `id`).  
- `[0]` — берём первый элемент строки — сам id.  

```python
    conn.commit()
```

- `commit()` — подтверждает изменения в базе, без него вставка не сохранится. [eax](https://eax.me/2019/2019-11-05-python-psycopg2.html)

```python
    cur.close()
    conn.close()
```

- Закрываем курсор и соединение, чтобы не держать лишние ресурсы. [geeksforgeeks](https://www.geeksforgeeks.org/python/how-to-close-connections-in-psycopg2-using-python/)

```python
    print("Добавлено, ID =", wid)
```

- Показываем пользователю номер созданной записи.  

***

### Функция 2: `show_all`

```python
def show_all():
    conn = connect()
    cur = conn.cursor()
```

- Подключение и создание курсора.

```python
    cur.execute(
        "SELECT id, exercise_name, training_date, sets, reps, "
        "weight_kg, difficulty, notes "
        "FROM training_logs ORDER BY training_date DESC"
    )
```

- `SELECT ... FROM training_logs` — выбирает нужные столбцы.  
- `ORDER BY training_date DESC` — сортировка по дате, последние тренировки сверху. [eax](https://eax.me/2019/2019-11-05-python-psycopg2.html)

```python
    for r in cur.fetchall():
        print(*r, sep=" | ")
```

- `fetchall()` — получить все строки результата.  
- `for r in ...` — перебираем строки.  
- `print(*r, sep=" | ")` — `*r` распаковывает элементы строки в аргументы print, `sep` задаёт разделитель.  

```python
    cur.close()
    conn.close()
```

- Закрытие ресурсов.  

***

### Функция 3: `search_ex`

```python
def search_ex(name):
    conn = connect()
    cur = conn.cursor()
```

- Подключение к базе.

```python
    cur.execute(
        """SELECT id, exercise_name, training_date, sets, reps,
                  weight_kg, difficulty, notes
           FROM training_logs
           WHERE lower(exercise_name) LIKE lower(%s)
           ORDER BY training_date DESC""",
        (f"%{name}%",)
    )
```

- `WHERE lower(exercise_name) LIKE lower(%s)` — поиск по названию, без учёта регистра. [habr](https://habr.com/ru/companies/bft/articles/777348/)
- `f"%{name}%"` — шаблон: содержит введённую строку (например `%жим%`).  
- Запятая в конце `( ..., )` — делает кортеж из одного элемента.  

Дальше цикл и закрытие — как в `show_all`.  

***

### Функция 4: `filter_date`

```python
def filter_date(d1, d2):
    conn = connect()
    cur = conn.cursor()
```

- Получает две даты: начало и конец.

```python
    cur.execute(
        """SELECT id, exercise_name, training_date, sets, reps,
                  weight_kg, difficulty, notes
           FROM training_logs
           WHERE training_date BETWEEN %s AND %s
           ORDER BY training_date""",
        (d1, d2)
    )
```

- `BETWEEN %s AND %s` — выбирает записи в указанном диапазоне дат включительно. [eax](https://eax.me/2019/2019-11-05-python-psycopg2.html)

Остальное — вывод и закрытие.  

***

### Функция 5: `update_workout`

```python
def update_workout(wid, w, notes):
    conn = connect()
    cur = conn.cursor()
```

- `wid` — id записи, `w` — новый вес, `notes` — новые заметки.

```python
    cur.execute(
        "UPDATE training_logs SET weight_kg=%s, notes=%s WHERE id=%s",
        (w, notes, wid)
    )
```

- `UPDATE ... SET ... WHERE id=%s` — изменение строки по её id.  

```python
    conn.commit()
    cur.close()
    conn.close()
    print("Обновлено")
```

- Подтверждаем изменения, закрываем, выводим сообщение.  

***

### Функция 6: `delete_workout`

```python
def delete_workout(wid):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM training_logs WHERE id=%s", (wid,))
    conn.commit()
    cur.close()
    conn.close()
    print("Удалено")
```

- Удаление строки по id через `DELETE`.  
- `(wid,)` — кортеж из одного значения.  
- `commit()` — подтверждение удаления.  

***

### Функция 7: `stats`

```python
def stats():
    conn = connect()
    cur = conn.cursor()
```

- Подключение к базе.

```python
    cur.execute(
        """SELECT count(*), max(weight_kg),
                  avg(weight_kg), avg(reps)
           FROM training_logs"""
    )
```

- `count(*)` — количество записей.  
- `max(weight_kg)` — максимальный вес.  
- `avg(weight_kg)` — средний вес.  
- `avg(reps)` — среднее число повторений. [eax](https://eax.me/2019/2019-11-05-python-psycopg2.html)

```python
    total, mx, avg_w, avg_r = cur.fetchone()
```

- Разбираем одну строку результата на четыре переменные.  

```python
    cur.close()
    conn.close()
```

- Закрываем соединение.

```python
    print("Всего записей:", total)
    print("Макс. вес:", mx)
    print("Средний вес:", round(avg_w or 0, 2))
    print("Средние повторы:", round(avg_r or 0, 2))
```

- `avg_w or 0` — если среднее `None` (нет строк), берём 0.  
- `round(..., 2)` — округляем до двух знаков после запятой.  

***

### Функция 8: `main` (консольное меню)

```python
def main():
    while True:
```

- Бесконечный цикл — меню показывается до выхода пользователя.

```python
        print("\n1 Добавить"
              "\n2 Показать все"
              "\n3 Поиск по упражнению"
              "\n4 Фильтр по дате"
              "\n5 Обновить запись"
              "\n6 Удалить запись"
              "\n7 Статистика"
              "\n0 Выход")
```

- Текстовое меню; `\n` — перевод строки.

```python
        cmd = input("Выбор: ")
```

- `input` читает строку с клавиатуры, `cmd` — выбранный пункт.

Блоки `if` / `elif`:

- `"1"` — собираем данные тренировки, приводим числа через `int` и `float`, берём дату или сегодняшнюю через `str(date.today())`, затем вызываем функцию 1 `add_workout(...)`.  
- `"2"` — вызов функции 2 `show_all()`.  
- `"3"` — функция 3 `search_ex(...)`.  
- `"4"` — функция 4 `filter_date(...)`.  
- `"5"` — функция 5 `update_workout(...)`.  
- `"6"` — функция 6 `delete_workout(...)`.  
- `"7"` — функция 7 `stats()`.  
- `"0"` — `break` выходит из цикла, программа заканчивается.  
- `else` — если введён неверный пункт, выводим сообщение.  

***

### Запуск файла

```python
if __name__ == "__main__":
    main()
```

- Проверка, что файл запущен напрямую, а не импортирован.  
- В этом случае вызывается `main()`, и стартует меню. [pythonlib](https://pythonlib.ru/library-theme53)

***

## Откуда взята информация

- Синтаксис psycopg2 (`connect`, `cursor`, `execute`, `fetchone`, `fetchall`, `commit`, `close`) и пример работы с PostgreSQL. [wiki.postgresql](https://wiki.postgresql.org/wiki/Psycopg2_Tutorial)
- Примеры простых консольных приложений с меню для работы с базой данных. [pcnews](https://pcnews.ru/blogs/pisem_konsolnoe_prilozenie_dla_raboty_s_bazoj_dannyh_na_python-1318800.html)
***
***
***
***
***
***
***
***
***
***
## SQL‑код для таблицы фильмов

```sql
CREATE TABLE movie_logs (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    watch_date DATE NOT NULL,
    duration_min INTEGER CHECK (duration_min > 0),
    rating INTEGER CHECK (rating BETWEEN 1 AND 10),
    genre TEXT CHECK (genre IN ('Боевик','Комедия','Драма','Фантастика','Другое')),
    review TEXT
);
```

- `CREATE TABLE movie_logs` — создаём таблицу с именем `movie_logs`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/170751200/9b9152a5-55cf-4948-b252-a41cb8741d52/5258242982513676994.jpg)
- `id SERIAL PRIMARY KEY` — поле `id` авто‑увеличивается (SERIAL) и является первичным ключом. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/170751200/9b9152a5-55cf-4948-b252-a41cb8741d52/5258242982513676994.jpg)
- `title TEXT NOT NULL` — текстовое название фильма, не может быть пустым. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/170751200/9b9152a5-55cf-4948-b252-a41cb8741d52/5258242982513676994.jpg)
- `watch_date DATE NOT NULL` — дата просмотра, тип `DATE`, тоже обязателен. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/170751200/9b9152a5-55cf-4948-b252-a41cb8741d52/5258242982513676994.jpg)
- `duration_min INTEGER CHECK (duration_min > 0)` — целое число минут, ограничение `CHECK` запрещает значения ≤ 0. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/170751200/9b9152a5-55cf-4948-b252-a41cb8741d52/5258242982513676994.jpg)
- `rating INTEGER CHECK (rating BETWEEN 1 AND 10)` — оценка целым числом от 1 до 10. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/170751200/9b9152a5-55cf-4948-b252-a41cb8741d52/5258242982513676994.jpg)
- `genre TEXT CHECK (genre IN (...))` — текст, но только из перечисленных жанров. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/170751200/9b9152a5-55cf-4948-b252-a41cb8741d52/5258242982513676994.jpg)
- `review TEXT` — свободный текст отзыва, без ограничений. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/170751200/9b9152a5-55cf-4948-b252-a41cb8741d52/5258242982513676994.jpg)

```sql
INSERT INTO movie_logs (title, watch_date, duration_min, rating, genre, review) VALUES
('Матрица', '2024-02-01', 136, 9, 'Фантастика', 'Классика'),
('Такси', '2024-02-05', 90, 7, 'Комедия', 'Весело'),
('Гладиатор', '2024-02-10', 155, 8, 'Драма', 'Сильно');
```

- `INSERT INTO movie_logs (...) VALUES` — вставляем начальные тестовые строки. [selectel](https://selectel.ru/blog/tutorials/postgresql-python/)
- В скобках указываем список столбцов, потом для каждой строки — значения в том же порядке. [selectel](https://selectel.ru/blog/tutorials/postgresql-python/)

***

## Python‑код: подключение к БД

```python
import psycopg2
from datetime import datetime
```

- `import psycopg2` — подключаем библиотеку для работы с PostgreSQL. [github](https://github.com/AndreyRysistov/PostgresHomework)
- `from datetime import datetime` — импортируем класс `datetime` (в этом коде он не обязателен, но обычно нужен для дат). [github](https://github.com/Vladimir127/TrainingDiary/blob/master/README.md)

```python
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname='21is6',
            user='postgres',
            password='1111',
            host='localhost'
        )
        print('База фильмов подключена')
        return conn
    except Exception as e:
        print(e)
        return None
```

- `def connect_db():` — объявление функции подключения к базе. [github](https://github.com/AndreyRysistov/PostgresHomework)
- `try:` — блок, где может возникнуть ошибка (например, база недоступна). [py.scilink](http://py.scilink.ru/4_6_database/)
- `psycopg2.connect(...)` — создаём соединение с БД, передаём имя базы, пользователя, пароль и хост. [github](https://github.com/AndreyRysistov/PostgresHomework)
- Параметр `dbname` — база; `user` — пользователь; `password` — пароль; `host` — адрес сервера. [github](https://github.com/AndreyRysistov/PostgresHomework)
- `print('База фильмов подключена')` — выводим сообщение, что всё ок.  
- `return conn` — возвращаем объект соединения для дальнейшей работы. [github](https://github.com/AndreyRysistov/PostgresHomework)
- `except Exception as e:` — ловим любую ошибку при подключении. [py.scilink](http://py.scilink.ru/4_6_database/)
- `print(e)` — печатаем текст ошибки.  
- `return None` — возвращаем `None`, чтобы вызывающая функция могла проверить, что подключения нет.  

***

## Функция add_movie

```python
def add_movie(title, date, duration, rating, genre, review):
    conn = connect_db()
    if not conn:
        return
```

- `def add_movie(...):` — функция добавления фильма, параметры совпадают с полями в таблице. [github](https://github.com/AndreyRysistov/PostgresHomework)
- `conn = connect_db()` — получаем соединение, вызывая предыдущую функцию.  
- `if not conn:` — если `connect_db` вернул `None`, просто выходим без работы.  

```python
    cur = conn.cursor()
```

- `cursor()` — создаём курсор для выполнения SQL‑запросов. [github](https://github.com/AndreyRysistov/PostgresHomework)

```python
    cur.execute(
        """INSERT INTO movie_logs
           (title, watch_date, duration_min, rating, genre, review)
           VALUES (%s,%s,%s,%s,%s,%s)""",
        (title, date, duration, rating, genre, review)
    )
```

- `cur.execute(...)` — отправляем SQL‑команду в базу. [github](https://github.com/AndreyRysistov/PostgresHomework)
- Многострочная строка `"""..."""` — удобная запись длинного запроса.  
- `INSERT INTO movie_logs (...)` — добавляем новую строку в таблицу. [selectel](https://selectel.ru/blog/tutorials/postgresql-python/)
- `VALUES (%s, ... )` — места для параметров; `%s` — placeholder для psycopg2. [github](https://github.com/AndreyRysistov/PostgresHomework)
- Второй аргумент `(... )` — кортеж с реальными значениями, которые безопасно подставятся в запрос. [github](https://github.com/AndreyRysistov/PostgresHomework)

```python
    conn.commit()
```

- `commit()` — сохраняет изменения в базе (без этого вставка останется только в транзакции). [github](https://github.com/AndreyRysistov/PostgresHomework)

```python
    cur.close()
    conn.close()
```

- `cur.close()` — закрываем курсор, чтобы освободить ресурсы. [github](https://github.com/AndreyRysistov/PostgresHomework)
- `conn.close()` — закрываем соединение с базой. [github](https://github.com/AndreyRysistov/PostgresHomework)

***

## Функция get_all_movies

```python
def get_all_movies():
    conn = connect_db()
    if not conn:
        return []
```

- Подключаемся к базе так же, как в `add_movie`.  
- Если соединения нет, возвращаем пустой список, чтобы `print_movies` мог нормально отработать.  

```python
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title, watch_date, duration_min, rating, genre, review "
        "FROM movie_logs ORDER BY watch_date DESC"
    )
```

- Создаём курсор.  
- `SELECT ... FROM movie_logs` — выбираем все нужные столбцы из таблицы. [eax](https://eax.me/2016/2016-07-18-python-postgresql.html)
- `ORDER BY watch_date DESC` — сортируем по дате просмотра, самые новые вверху. [eax](https://eax.me/2016/2016-07-18-python-postgresql.html)

```python
    movies = cur.fetchall()
```

- `fetchall()` — получаем все строки результата в виде списка кортежей. [github](https://github.com/AndreyRysistov/PostgresHomework)

```python
    cur.close()
    conn.close()
    return movies
```

- Закрываем курсор и соединение и возвращаем список фильмов.  

***

## Функция search_by_title

```python
def search_by_title(movie_title):
    conn = connect_db()
    if not conn:
        return []
    cur = conn.cursor()
```

- Подключение и создание курсора — тот же шаблон.  

```python
    cur.execute(
        """SELECT id, title, watch_date, duration_min, rating, genre, review
           FROM movie_logs
           WHERE lower(title) LIKE lower(%s)
           ORDER BY watch_date DESC""",
        (f"%{movie_title}%",)
    )
```

- `WHERE lower(title) LIKE lower(%s)` — сравниваем названия без учёта регистра. [eax](https://eax.me/2016/2016-07-18-python-postgresql.html)
- `LIKE` с шаблоном `%...%` ищет вхождение подстроки в строке. [eax](https://eax.me/2016/2016-07-18-python-postgresql.html)
- `f"%{movie_title}%"` — f‑строка: добавляем `%` по краям введённого названия.  
- `( ..., )` — кортеж из одного элемента (так требует `execute`). [github](https://github.com/AndreyRysistov/PostgresHomework)

```python
    movies = cur.fetchall()
    cur.close()
    conn.close()
    return movies
```

- Берём все подходящие фильмы и возвращаем как список.  

***

## Функция filter_by_rating

```python
def filter_by_rating(min_rating):
    conn = connect_db()
    if not conn:
        return []
    cur = conn.cursor()
```

- Аналогично, подключаемся.  

```python
    cur.execute(
        """SELECT id, title, watch_date, duration_min, rating, genre, review
           FROM movie_logs
           WHERE rating >= %s
           ORDER BY rating DESC""",
        (min_rating,)
    )
```

- `WHERE rating >= %s` — выбираем фильмы с оценкой не ниже заданной. [eax](https://eax.me/2016/2016-07-18-python-postgresql.html)
- `ORDER BY rating DESC` — сортируем по убыванию рейтинга, от лучших к худшим. [eax](https://eax.me/2016/2016-07-18-python-postgresql.html)
- `(min_rating,)` — кортеж с одним параметром.  

```python
    movies = cur.fetchall()
    cur.close()
    conn.close()
    return movies
```

- Возвращаем отфильтрованный список.  

***

## Функция update_movie

```python
def update_movie(log_id, new_rating, new_review):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
```

- Подключение к базе, если не удалось — просто выходим.  

```python
    cur.execute(
        "UPDATE movie_logs SET rating=%s, review=%s WHERE id=%s",
        (new_rating, new_review, log_id)
    )
```

- `UPDATE movie_logs SET ... WHERE id=%s` — обновляем строку с нужным `id`. [selectel](https://selectel.ru/blog/tutorials/postgresql-python/)
- Меняем оценку и отзыв на новые значения.  

```python
    conn.commit()
    cur.close()
    conn.close()
```

- Подтверждаем изменения и закрываем соединение.  

***

## Функция delete_movie

```python
def delete_movie(log_id):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
```

- Подключение.  

```python
    cur.execute("DELETE FROM movie_logs WHERE id=%s", (log_id,))
```

- `DELETE FROM movie_logs WHERE id=%s` — удаляем одну запись по её ID. [selectel](https://selectel.ru/blog/tutorials/postgresql-python/)
- `(log_id,)` — кортеж с параметром.  

```python
    conn.commit()
    cur.close()
    conn.close()
```

- Сохраняем и закрываем.  

***

## Функция get_cinema_stats

```python
def get_cinema_stats():
    conn = connect_db()
    if not conn:
        return {}
    cur = conn.cursor()
```

- Подключаемся; если не получилось — возвращаем пустой словарь, чтобы меню не упало.  

```python
    cur.execute(
        """SELECT COUNT(*), COALESCE(AVG(rating),0), COALESCE(SUM(duration_min),0)
           FROM movie_logs"""
    )
    count, avg_r, total_min = cur.fetchone()
```

- `SELECT COUNT(*), AVG(rating), SUM(duration_min)` — считаем количество фильмов, среднюю оценку и суммарную длительность в минутах. [github](https://github.com/xanhex/fitness-tracker)
- `COALESCE(AVG(rating),0)` — если фильмов нет и `AVG` вернёт `NULL`, подставляем 0. [github](https://github.com/xanhex/fitness-tracker)
- `cur.fetchone()` — получаем одну строку результата и раскладываем её в три переменные.  

```python
    cur.execute(
        """SELECT genre
           FROM movie_logs
           GROUP BY genre
           ORDER BY COUNT(*) DESC
           LIMIT 1"""
    )
```

- `GROUP BY genre` — группируем записи по жанру. [github](https://github.com/xanhex/fitness-tracker)
- `ORDER BY COUNT(*) DESC` — сортируем группы по количеству фильмов, от большего к меньшему. [github](https://github.com/xanhex/fitness-tracker)
- `LIMIT 1` — берём только первую строку — самый популярный жанр.  

```python
    row = cur.fetchone()
    popular = row[0] if row else 'Нет данных'
```

- Если `fetchone()` вернул строку — берём жанр `row[0]`, иначе ставим строку `'Нет данных'`.  

```python
    cur.close()
    conn.close()
```

- Закрываем курсор и соединение.  

```python
    return {
        'count': count,
        'avg_rating': round(avg_r, 2),
        'total_hours': round(total_min / 60, 1),
        'popular_genre': popular
    }
```

- Возвращаем словарь со статистикой.  
- `round(avg_r, 2)` — округляем средний рейтинг до двух знаков после запятой.  
- `total_min / 60` — переводим минуты в часы, `round(..., 1)` оставляет один знак после запятой.  

***

## Функция print_movies

```python
def print_movies(movies):
    if not movies:
        print('Пора начать смотреть кино!')
        return
```

- Функция печати списка фильмов.  
- Если список пустой (`not movies`), выводим сообщение и выходим.  

```python
    for m in movies:
        print(f"{m [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/170751200/9b9152a5-55cf-4948-b252-a41cb8741d52/5258242982513676994.jpg)} ({m [selectel](https://selectel.ru/blog/tutorials/postgresql-python/)}) - Оценка: {m [github](https://github.com/Vladimir127/TrainingDiary/blob/master/README.md)}/10")
```

- `for m in movies:` — перебираем каждый кортеж с данными фильма.  
- `m [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/170751200/9b9152a5-55cf-4948-b252-a41cb8741d52/5258242982513676994.jpg)` — `title`, `m [selectel](https://selectel.ru/blog/tutorials/postgresql-python/)` — `watch_date`, `m [github](https://github.com/Vladimir127/TrainingDiary/blob/master/README.md)` — `rating` (порядок соответствует `SELECT`).  
- f‑строка форматирует красивый вывод: «Название (дата) — Оценка: 8/10».  

***

## Про источники (условно)

1. Основной синтаксис SQL `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`, `GROUP BY`, `ORDER BY`, `COUNT`, `AVG`, `SUM`, `COALESCE` — стандарт SQL, учебники по SQL. [github](https://github.com/xanhex/fitness-tracker)
2. Использование `psycopg2.connect`, `cursor`, `execute`, `fetchone`, `fetchall`, `commit`, `close`, параметров `%s` — документация psycopg2 и типичные примеры CRUD в Python. [eax](https://eax.me/2016/2016-07-18-python-postgresql.html)
3. Конструкция `try/except`, управление функциями и циклами, f‑строки — базовый синтаксис Python. [py.scilink](http://py.scilink.ru/4_6_database/)

Если хочешь, могу также кратко описать, как каждую функцию объяснить устно преподавателю (типа «Функция 1 делает вставку, 2 — выводит все фильмы»).
***
***
***
***
***
Кратко, как можно устно рассказать каждую функцию (по номерам, как раньше):

1. **Функция подключения `connect_db`**  
   «Эта функция открывает соединение с базой `21is6` через psycopg2 и возвращает объект соединения. Если подключиться не получается (неверный пароль, база выключена), я ловлю ошибку и возвращаю `None`, чтобы остальные функции не падали.» [psycopg](https://www.psycopg.org/docs/usage.html)

2. **Функция `add_movie` (добавление фильма)**  
   «Получает параметры фильма из меню и делает `INSERT` в таблицу `movie_logs`: записывает название, дату просмотра, длительность, оценку, жанр и отзыв. После вставки вызывает `commit`, чтобы изменения сохранились, и закрывает соединение.» [pythonru](https://pythonru.com/biblioteki/operacii-insert-update-delete-v-postgresql)

3. **Функция `get_all_movies` (показать все)**  
   «Подключается к базе, выполняет `SELECT` всех столбцов из `movie_logs`, сортирует фильмы по дате просмотра от новых к старым и возвращает список строк. Если нет подключения — возвращает пустой список.» [pythonru](https://pythonru.com/biblioteki/posgresql-python-select)

4. **Функция `search_by_title` (поиск по названию)**  
   «Делает выборку фильмов, у которых название содержит введённую строку. Использую `WHERE lower(title) LIKE lower('%строка%')`, чтобы поиск не зависел от регистра. Результат сортируется по дате и возвращается как список.» [pythonru](https://pythonru.com/biblioteki/posgresql-python-select)

5. **Функция `filter_by_rating` (фильтр по рейтингу)**  
   «Выбирает все фильмы, у которых оценка больше или равна указанному минимуму. В запросе `WHERE rating >= ?` и сортировка `ORDER BY rating DESC`, чтобы сначала показывать самые высокие оценки.» [digitalocean](https://www.digitalocean.com/community/tutorials/how-to-use-groupby-and-orderby-in-sql)

6. **Функция `update_movie` (обновление оценки и отзыва)**  
   «По ID фильма обновляет два поля: `rating` и `review`. Для этого использую запрос `UPDATE movie_logs SET rating = ..., review = ... WHERE id = ...`. Потом делаю `commit` и закрываю соединение.» [pythonru](https://pythonru.com/biblioteki/operacii-insert-update-delete-v-postgresql)

7. **Функция `delete_movie` (удаление фильма)**  
   «Удаляет запись по её ID с помощью `DELETE FROM movie_logs WHERE id = ...`. Также делаю `commit`, чтобы удаление применилось.» [pythonru](https://pythonru.com/biblioteki/operacii-insert-update-delete-v-postgresql)

8. **Функция `get_cinema_stats` (статистика)**  
   «Возвращает словарь с общей статистикой по фильмотеке. В первом запросе считаю количество фильмов, средний рейтинг и сумму продолжительности в минутах (`COUNT`, `AVG`, `SUM`). Во втором запросе через `GROUP BY genre` и `ORDER BY COUNT(*) DESC LIMIT 1` нахожу жанр, который встречается чаще всего. Перевожу общее время из минут в часы и округляю числа.» [wiki.merionet](https://wiki.merionet.ru/articles/tutorial-sql-po-gruppirovke-obieiasniaem-komandy-count-sum-average-i-having)

9. **Функция `print_movies` (печать списка)**  
   «Получает список фильмов из любой из предыдущих функций. Если список пустой — выводит фразу, что пора начинать смотреть кино. Если нет — для каждой записи печатает название, дату и оценку в формате `Название (Дата) – Оценка: 8/10`. Эта функция отдельно занимается только выводом, чтобы код не дублировался.» [pythonru](https://pythonru.com/biblioteki/posgresql-python-select)

10. **Функция `main` и меню**  
    «В `main` у меня бесконечный цикл с текстовым меню. В зависимости от введённого номера я запрашиваю у пользователя нужные данные и вызываю одну из функций сверху. Пункт 8 завершает цикл через `break`. Так получается простое консольное приложение, которое покрывает все пункты ТЗ: добавление, просмотр, поиск, фильтр, обновление, удаление и статистика.» [habr](https://habr.com/ru/companies/bft/articles/777348/)

Этого обычно достаточно, чтобы на защите уверенно рассказать, что делает каждая часть программы и как она работает с базой.
