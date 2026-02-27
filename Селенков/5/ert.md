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
Ниже только те функции, которые я добавил (их реализация), и краткое объяснение, что каждая делает и зачем нужна. Источники — учебные материалы по SQL и psycopg2, помечаю условными ссылками. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/170751200/9b9152a5-55cf-4948-b252-a41cb8741d52/5258242982513676994.jpg)

***

## Функция `add_movie`

```python
def add_movie(title, date, duration, rating, genre, review):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO movie_logs
           (title, watch_date, duration_min, rating, genre, review)
           VALUES (%s,%s,%s,%s,%s,%s)""",
        (title, date, duration, rating, genre, review)
    )
    conn.commit()
    cur.close()
    conn.close()
```

- Берёт данные фильма из аргументов и вставляет их в таблицу `movie_logs` через запрос `INSERT`.  
- Использует плейсхолдеры `%s` и передачу параметров кортежем, чтобы не было SQL‑инъекций.  
- После `execute` вызывает `commit`, чтобы изменения сохранились в базе, и обязательно закрывает курсор и соединение.  
 [selectel](https://selectel.ru/blog/tutorials/postgresql-python/)

***

## Функция `get_all_movies`

```python
def get_all_movies():
    conn = connect_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title, watch_date, duration_min, rating, genre, review "
        "FROM movie_logs ORDER BY watch_date DESC"
    )
    movies = cur.fetchall()
    cur.close()
    conn.close()
    return movies
```

- Делает простой `SELECT` всех нужных столбцов из `movie_logs`.  
- Сортирует фильмы по дате просмотра от новых к старым (`ORDER BY watch_date DESC`).  
- Забирает все строки через `fetchall` и возвращает список кортежей в вызывающий код.  
 [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/170751200/9b9152a5-55cf-4948-b252-a41cb8741d52/5258242982513676994.jpg)

***

## Функция `search_by_title`

```python
def search_by_title(movie_title):
    conn = connect_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute(
        """SELECT id, title, watch_date, duration_min, rating, genre, review
           FROM movie_logs
           WHERE lower(title) LIKE lower(%s)
           ORDER BY watch_date DESC""",
        (f"%{movie_title}%",)
    )
    movies = cur.fetchall()
    cur.close()
    conn.close()
    return movies
```

- Ищет фильмы по подстроке в названии: в `WHERE` используется `LOWER(title) LIKE LOWER('%строка%')`, чтобы регистр букв не имел значения.  
- Шаблон `"%...%"` позволяет найти совпадение в середине строки, а не только в начале или конце.  
- Возвращает только те фильмы, у которых название подходит под условие, также отсортированные по дате.  
 [selectel](https://selectel.ru/blog/tutorials/postgresql-python/)

***

## Функция `filter_by_rating`

```python
def filter_by_rating(min_rating):
    conn = connect_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute(
        """SELECT id, title, watch_date, duration_min, rating, genre, review
           FROM movie_logs
           WHERE rating >= %s
           ORDER BY rating DESC""",
        (min_rating,)
    )
    movies = cur.fetchall()
    cur.close()
    conn.close()
    return movies
```

- Выбирает фильмы с рейтингом не ниже заданного минимума (`rating >= ?`).  
- Сортирует результат по убыванию рейтинга, чтобы сначала показывать самые высоко оценённые.  
- Возвращает список подходящих фильмов, с которыми дальше работает меню.  
 [github](https://github.com/AndreyRysistov/PostgresHomework)

***

## Функция `update_movie`

```python
def update_movie(log_id, new_rating, new_review):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute(
        "UPDATE movie_logs SET rating=%s, review=%s WHERE id=%s",
        (new_rating, new_review, log_id)
    )
    conn.commit()
    cur.close()
    conn.close()
```

- По ID фильма обновляет два поля — оценку и отзыв — с помощью запроса `UPDATE ... SET ... WHERE id = ?`.  
- Параметры передаются как кортеж, чтобы избежать ручной склейки строки SQL.  
- После обновления выполняет `commit`, чтобы изменения записались в базу.  
 [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/170751200/9b9152a5-55cf-4948-b252-a41cb8741d52/5258242982513676994.jpg)

***

## Функция `delete_movie`

```python
def delete_movie(log_id):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("DELETE FROM movie_logs WHERE id=%s", (log_id,))
    conn.commit()
    cur.close()
    conn.close()
```

- Удаляет одну запись из таблицы по её ID через `DELETE FROM movie_logs WHERE id = ?`.  
- Использует параметр `%s` вместо подстановки ID в строку, чтобы запрос был безопасным и аккуратным.  
- Подтверждает удаление `commit` и закрывает соединение.  
 [selectel](https://selectel.ru/blog/tutorials/postgresql-python/)

***

## Функция `get_cinema_stats`

```python
def get_cinema_stats():
    conn = connect_db()
    if not conn:
        return {}
    cur = conn.cursor()

    cur.execute(
        """SELECT COUNT(*), COALESCE(AVG(rating),0), COALESCE(SUM(duration_min),0)
           FROM movie_logs"""
    )
    count, avg_r, total_min = cur.fetchone()

    cur.execute(
        """SELECT genre
           FROM movie_logs
           GROUP BY genre
           ORDER BY COUNT(*) DESC
           LIMIT 1"""
    )
    row = cur.fetchone()
    popular = row[0] if row else 'Нет данных'

    cur.close()
    conn.close()

    return {
        'count': count,
        'avg_rating': round(avg_r, 2),
        'total_hours': round(total_min / 60, 1),
        'popular_genre': popular
    }
```

- В первом запросе считает:  
  - количество фильмов (`COUNT(*)`),  
  - среднюю оценку (`AVG(rating)`),  
  - суммарную длительность (`SUM(duration_min)`).  
- `COALESCE(..., 0)` подставляет 0 вместо `NULL`, если таблица пустая.  
- Во втором запросе через `GROUP BY genre` и `ORDER BY COUNT(*) DESC LIMIT 1` определяется жанр, который встречается чаще всего.  
- После получения данных закрывает соединение и возвращает словарь: число фильмов, средний рейтинг, общее время в часах и популярный жанр.  
 [github](https://github.com/AndreyRysistov/PostgresHomework)

***

## Функция `print_movies`

```python
def print_movies(movies):
    if not movies:
        print('Пора начать смотреть кино!')
        return
    for m in movies:
        print(f"{m [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/170751200/9b9152a5-55cf-4948-b252-a41cb8741d52/5258242982513676994.jpg)} ({m [selectel](https://selectel.ru/blog/tutorials/postgresql-python/)}) - Оценка: {m[4]}/10")
```

- Отвечает только за вывод фильмов на экран, чтобы логика печати не дублировалась в меню.  
- Если список пустой, пишет сообщение и заканчивает работу.  
- Если нет — для каждой строки печатает название, дату и оценку в понятном формате через f‑строку.  
 [github](https://github.com/AndreyRysistov/PostgresHomework)

***

Условные источники:  
-  — учебники/конспекты по SQL (INSERT, SELECT, UPDATE, DELETE, COUNT, AVG, SUM, GROUP BY, ORDER BY, COALESCE). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/170751200/9b9152a5-55cf-4948-b252-a41cb8741d52/5258242982513676994.jpg)
-  — документация и примеры psycopg2 (connect, cursor, execute, fetchone/fetchall, commit, параметризованные запросы). [selectel](https://selectel.ru/blog/tutorials/postgresql-python/)
-  — базовый Python: функции, условия, циклы, обработка списков, f‑строки. [github](https://github.com/AndreyRysistov/PostgresHomework)
