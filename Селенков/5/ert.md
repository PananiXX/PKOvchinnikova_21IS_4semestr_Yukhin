## Разбор кода построчно:

```python
import psycopg2
```
- **import** - команда чтобы подключить готовый код
- **psycopg2** - библиотека для работы с PostgreSQL

```python
from datetime import datetime
```
- **from** - взять из
- **datetime** - библиотека для работы с датами
- **import datetime** - взять только функцию datetime

---

```python
def connect_db():
```
- **def** - создать функцию
- **connect_db** - название функции

```python
    try:
```
- **try** - попробовать выполнить код

```python
        conn = psycopg2.connect(
```
- **conn** - переменная для подключения
- **psycopg2.connect()** - функция подключения к БД

```python
            database="workout_db",
```
- **database** - имя базы данных
- **"workout_db"** - название БД

```python
            user="postgres",
```
- **user** - имя пользователя
- **"postgres"** - стандартный пользователь

```python
            password="1111",
```
- **password** - пароль
- **"1111"** - сам пароль

```python
            host="localhost"
```
- **host** - где находится БД
- **"localhost"** - на этом же компьютере

```python
        )
        print("Подключение успешно")
```
- **print()** - вывести текст на экран

```python
        return conn
```
- **return** - вернуть результат
- **conn** - само подключение

```python
    except:
```
- **except** - если в try была ошибка

```python
        print("Ошибка подключения")
        return None
```
- **None** - ничего (пустота)

---

```python
def add_workout(conn):
```
- **add_workout** - добавить тренировку
- **(conn)** - функция принимает подключение

```python
    print("\n--- Добавление тренировки ---")
```
- **\n** - новая строка

```python
    name = input("Упражнение: ")
```
- **name** - переменная для названия
- **input()** - спросить у пользователя

```python
    date = input("Дата (ГГГГ-ММ-ДД), Enter если сегодня: ")
    if date == "":
```
- **if** - если
- **date == ""** - если строка пустая (нажали Enter)

```python
        now = datetime.now()
```
- **now** - текущий момент
- **datetime.now()** - получить текущую дату и время

```python
        date = f"{now.year}-{now.month}-{now.day}"
```
- **f"..."** - форматированная строка
- **now.year** - текущий год
- **now.month** - месяц
- **now.day** - день

```python
    try:
        sets = int(input("Подходы: "))
```
- **int()** - превратить в целое число

```python
        reps = int(input("Повторения: "))
        weight = float(input("Вес: "))
```
- **float()** - превратить в дробное число

```python
    except:
        print("Ошибка! Нужны цифры!")
        return
```
- **return** без значения - выйти из функции

```python
    diff = input("Сложность (легко/нормально/тяжело): ")
    notes = input("Заметки: ")
```

```python
    cur = conn.cursor()
```
- **cur** - курсор (штука для запросов)
- **cursor()** - создать курсор

```python
    cur.execute("INSERT INTO training_logs VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                (name, date, sets, reps, weight, diff, notes))
```
- **execute()** - выполнить SQL запрос
- **INSERT INTO** - добавить в таблицу
- **training_logs** - название таблицы
- **VALUES** - значения
- **%s** - места для подстановки
- **(..., ...)** - кортеж с данными

```python
    conn.commit()
```
- **commit()** - сохранить изменения

```python
    cur.close()
```
- **close()** - закрыть курсор

```python
    print("Добавлено!")
```

---

```python
def get_all_workouts(conn):
    print("\n--- Все тренировки ---")
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM training_logs")
```
- **SELECT * FROM** - взять всё из таблицы

```python
    rows = cur.fetchall()
```
- **fetchall()** - получить все строки

```python
    if len(rows) == 0:
```
- **len()** - длина (количество)

```python
        print("Нет записей!")
        cur.close()
        return
    
    for r in rows:
```
- **for** - цикл
- **r** - одна запись
- **in rows** - в списке rows

```python
        print(f"{r[2]} | {r[1]} | {r[3]}x{r[4]} | {r[5]}кг")
```
- **r[2]** - третий элемент (индексы с 0)
- **|** - просто разделитель

```python
    cur.close()
```

---

```python
def search_by_exercise(conn):
    print("\n--- Поиск ---")
    
    name = input("Название: ")
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM training_logs WHERE exercise_name = %s", (name,))
```
- **WHERE** - условие
- **exercise_name = %s** - название равно

```python
    rows = cur.fetchall()
    
    if len(rows) == 0:
        print("Ничего нет")
    else:
        for r in rows:
            print(f"{r[2]} | {r[1]} | {r[3]}x{r[4]} | {r[5]}кг")
    cur.close()
```

---

```python
def filter_by_date(conn):
    print("\n--- Фильтр по дате ---")
    
    start = input("От: ")
    end = input("До: ")
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM training_logs WHERE training_date >= %s AND training_date <= %s", (start, end))
```
- **>=** - больше или равно
- **<=** - меньше или равно
- **AND** - и (оба условия)

```python
    rows = cur.fetchall()
    
    if len(rows) == 0:
        print("Записей нет")
    else:
        for r in rows:
            print(f"{r[2]} | {r[1]} | {r[3]}x{r[4]} | {r[5]}кг")
    cur.close()
```

---

```python
def update_workout(conn):
    print("\n--- Обновление ---")
    
    id = input("ID: ")
    weight = input("Новый вес: ")
    reps = input("Новые повторения: ")
    
    cur = conn.cursor()
    cur.execute("UPDATE training_logs SET weight_kg = %s, reps = %s WHERE id = %s", (weight, reps, id))
```
- **UPDATE** - обновить
- **SET** - установить
- **weight_kg = %s** - поле вес = 
- **WHERE id = %s** - где айди =

```python
    conn.commit()
    cur.close()
    print("Обновлено!")
```

---

```python
def delete_workout(conn):
    print("\n--- Удаление ---")
    
    id = input("ID: ")
    
    cur = conn.cursor()
    cur.execute("DELETE FROM training_logs WHERE id = %s", (id,))
```
- **DELETE FROM** - удалить из

```python
    conn.commit()
    cur.close()
    print("Удалено!")
```

---

```python
def get_progress_stats(conn):
    print("\n--- СТАТИСТИКА ---")
    
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM training_logs")
```
- **COUNT(*)** - посчитать количество строк

```python
    total = cur.fetchone()[0]
```
- **fetchone()** - получить одну строку
- **[0]** - первый элемент

```python
    print(f"Всего записей: {total}")
    
    cur.execute("SELECT MAX(weight_kg) FROM training_logs")
```
- **MAX()** - максимальное значение

```python
    max_w = cur.fetchone()[0]
    print(f"Макс вес: {max_w} кг")
    
    cur.execute("SELECT AVG(sets) FROM training_logs")
```
- **AVG()** - среднее значение

```python
    avg_s = cur.fetchone()[0]
    print(f"Среднее подходов: {avg_s}")
    
    cur.close()
```

---

```python
def menu():
    conn = connect_db()
    if conn == None:
        return
    
    while True:
```
- **while True:** - бесконечный цикл

```python
        print("\nМЕНЮ:")
        print("1 - Добавить")
        print("2 - Показать все")
        print("3 - Поиск")
        print("4 - Фильтр по дате")
        print("5 - Обновить")
        print("6 - Удалить")
        print("7 - Статистика")
        print("0 - Выход")
        
        choice = input("Выбери: ")
        
        if choice == "1":
            add_workout(conn)
        elif choice == "2":
            get_all_workouts(conn)
        elif choice == "3":
            search_by_exercise(conn)
        elif choice == "4":
            filter_by_date(conn)
        elif choice == "5":
            update_workout(conn)
        elif choice == "6":
            delete_workout(conn)
        elif choice == "7":
            get_progress_stats(conn)
        elif choice == "0":
            print("Пока!")
            break
```
- **break** - выйти из цикла

```python
        else:
            print("Неправильно!")
    
    conn.close()
```
- **close()** - закрыть подключение

```python
menu()
```
- Запустить функцию menu

Вот и всё! Каждая строчка что-то делает ☝️

## ЧТО ТАКОЕ ФУНКЦИЯ?

**Функция** - это кусок кода, который можно вызвать по имени. Как рецепт: ты один раз записываешь рецепт (создаешь функцию), а потом можешь готовить по нему сколько хочешь (вызывать функцию).

Пример из жизни:
- Функция "сварить_кофе" - налил воду, насыпал кофе, включил кнопку
- Когда хочешь кофе - говоришь "сварить_кофе()" и он готов

В программе то же самое: написал код один раз, а вызываешь когда нужно.

---

## ВСЕГО ФУНКЦИЙ В КОДЕ: 9 ШТУК

### Функция №1: `connect_db()`
```python
def connect_db():
    try:
        conn = psycopg2.connect(
            database="workout_db",
            user="postgres",
            password="1111",
            host="localhost"
        )
        print("Подключение успешно")
        return conn
    except:
        print("Ошибка подключения")
        return None
```
**Что делает:** Подключается к базе данных
- `def` - создать функцию
- `connect_db` - имя функции (соединиться с БД)
- `()` - скобки (функция без входных данных)
- `:` - начало функции
- `try:` - попробуй выполнить
- `conn = psycopg2.connect(...)` - переменная conn = подключение к БД
- `database="workout_db"` - имя базы
- `user="postgres"` - логин
- `password="1111"` - пароль
- `host="localhost"` - на этом компе
- `print("Подключение успешно")` - вывести текст
- `return conn` - вернуть подключение
- `except:` - если ошибка
- `print("Ошибка подключения")` - вывести ошибку
- `return None` - вернуть пустоту

---

### Функция №2: `add_workout(conn)`
```python
def add_workout(conn):
    print("\n--- Добавление тренировки ---")
    
    name = input("Упражнение: ")
    date = input("Дата (ГГГГ-ММ-ДД), Enter если сегодня: ")
    if date == "":
        now = datetime.now()
        date = f"{now.year}-{now.month}-{now.day}"
    
    try:
        sets = int(input("Подходы: "))
        reps = int(input("Повторения: "))
        weight = float(input("Вес: "))
    except:
        print("Ошибка! Нужны цифры!")
        return
    
    diff = input("Сложность (легко/нормально/тяжело): ")
    notes = input("Заметки: ")
    
    cur = conn.cursor()
    cur.execute("INSERT INTO training_logs (exercise_name, training_date, sets, reps, weight_kg, difficulty, notes) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                (name, date, sets, reps, weight, diff, notes))
    conn.commit()
    cur.close()
    
    print("Добавлено!")
```
**Что делает:** Добавляет новую тренировку в базу
- `def add_workout(conn):` - функция с входным параметром conn (подключение)
- `print("\n--- Добавление тренировки ---")` - заголовок
- `name = input("Упражнение: ")` - спросить и сохранить в name
- `date = input("Дата... ")` - спросить дату
- `if date == "":` - если ничего не ввели
- `now = datetime.now()` - взять текущее время
- `date = f"{now.year}-{now.month}-{now.day}"` - сделать строку с датой
- `try:` - попробуй
- `sets = int(input("Подходы: "))` - спросить и сделать числом
- `reps = int(input("Повторения: "))` - повторения
- `weight = float(input("Вес: "))` - вес
- `except:` - если ошибка
- `print("Ошибка! Нужны цифры!")` - вывести
- `return` - выйти из функции
- `diff = input("Сложность... ")` - сложность
- `notes = input("Заметки: ")` - заметки
- `cur = conn.cursor()` - создать курсор
- `cur.execute("INSERT...", (данные))` - выполнить запрос на добавление
- `conn.commit()` - сохранить
- `cur.close()` - закрыть курсор
- `print("Добавлено!")` - сообщить

---

### Функция №3: `get_all_workouts(conn)`
```python
def get_all_workouts(conn):
    print("\n--- Все тренировки ---")
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM training_logs")
    rows = cur.fetchall()
    
    if len(rows) == 0:
        print("Нет записей!")
        cur.close()
        return
    
    for r in rows:
        print(f"{r[2]} | {r[1]} | {r[3]}x{r[4]} | {r[5]}кг")
    cur.close()
```
**Что делает:** Показывает все тренировки
- `cur.execute("SELECT * FROM training_logs")` - взять всё из таблицы
- `rows = cur.fetchall()` - сохранить все строки в rows
- `if len(rows) == 0:` - если строк 0 (пусто)
- `for r in rows:` - для каждой строки в rows
- `print(f"{r[2]} | {r[1]} | {r[3]}x{r[4]} | {r[5]}кг")` - вывести дату, упражнение, подходыxповторы, вес

---

### Функция №4: `search_by_exercise(conn)`
```python
def search_by_exercise(conn):
    print("\n--- Поиск ---")
    
    name = input("Название: ")
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM training_logs WHERE exercise_name = %s", (name,))
    rows = cur.fetchall()
    
    if len(rows) == 0:
        print("Ничего нет")
    else:
        for r in rows:
            print(f"{r[2]} | {r[1]} | {r[3]}x{r[4]} | {r[5]}кг")
    cur.close()
```
**Что делает:** Ищет тренировки по названию
- `WHERE exercise_name = %s` - условие: название упражнения равно
- `(name,)` - значение для подстановки

---

### Функция №5: `filter_by_date(conn)`
```python
def filter_by_date(conn):
    print("\n--- Фильтр по дате ---")
    
    start = input("От: ")
    end = input("До: ")
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM training_logs WHERE training_date >= %s AND training_date <= %s", (start, end))
    rows = cur.fetchall()
    
    if len(rows) == 0:
        print("Записей нет")
    else:
        for r in rows:
            print(f"{r[2]} | {r[1]} | {r[3]}x{r[4]} | {r[5]}кг")
    cur.close()
```
**Что делает:** Показывает тренировки за период
- `WHERE training_date >= %s AND training_date <= %s` - дата больше или равна И дата меньше или равна

---

### Функция №6: `update_workout(conn)`
```python
def update_workout(conn):
    print("\n--- Обновление ---")
    
    id = input("ID: ")
    weight = input("Новый вес: ")
    reps = input("Новые повторения: ")
    
    cur = conn.cursor()
    cur.execute("UPDATE training_logs SET weight_kg = %s, reps = %s WHERE id = %s", (weight, reps, id))
    conn.commit()
    cur.close()
    print("Обновлено!")
```
**Что делает:** Обновляет вес и повторения
- `UPDATE training_logs SET` - обновить таблицу, установить
- `weight_kg = %s` - вес = 
- `reps = %s` - повторения = 
- `WHERE id = %s` - где айди =

---

### Функция №7: `delete_workout(conn)`
```python
def delete_workout(conn):
    print("\n--- Удаление ---")
    
    id = input("ID: ")
    
    cur = conn.cursor()
    cur.execute("DELETE FROM training_logs WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    print("Удалено!")
```
**Что делает:** Удаляет тренировку
- `DELETE FROM training_logs` - удалить из таблицы
- `WHERE id = %s` - где айди =

---

### Функция №8: `get_progress_stats(conn)`
```python
def get_progress_stats(conn):
    print("\n--- СТАТИСТИКА ---")
    
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM training_logs")
    total = cur.fetchone()[0]
    print(f"Всего записей: {total}")
    
    cur.execute("SELECT MAX(weight_kg) FROM training_logs")
    max_w = cur.fetchone()[0]
    print(f"Макс вес: {max_w} кг")
    
    cur.execute("SELECT AVG(sets) FROM training_logs")
    avg_s = cur.fetchone()[0]
    print(f"Среднее подходов: {avg_s}")
    
    cur.close()
```
**Что делает:** Показывает статистику
- `SELECT COUNT(*)` - посчитать количество
- `SELECT MAX(weight_kg)` - найти максимальный вес
- `SELECT AVG(sets)` - найти среднее подходов
- `cur.fetchone()[0]` - взять первый элемент из первой строки

---

### Функция №9: `menu()`
```python
def menu():
    conn = connect_db()
    if conn == None:
        return
    
    while True:
        print("\nМЕНЮ:")
        print("1 - Добавить")
        print("2 - Показать все")
        print("3 - Поиск")
        print("4 - Фильтр по дате")
        print("5 - Обновить")
        print("6 - Удалить")
        print("7 - Статистика")
        print("0 - Выход")
        
        choice = input("Выбери: ")
        
        if choice == "1":
            add_workout(conn)
        elif choice == "2":
            get_all_workouts(conn)
        elif choice == "3":
            search_by_exercise(conn)
        elif choice == "4":
            filter_by_date(conn)
        elif choice == "5":
            update_workout(conn)
        elif choice == "6":
            delete_workout(conn)
        elif choice == "7":
            get_progress_stats(conn)
        elif choice == "0":
            print("Пока!")
            break
        else:
            print("Неправильно!")
    
    conn.close()
```
**Что делает:** Главное меню программы
- `conn = connect_db()` - вызвать функцию №1 (подключиться)
- `if conn == None:` - если не подключились
- `return` - выйти
- `while True:` - бесконечный цикл
- `choice = input("Выбери: ")` - спросить цифру
- `if choice == "1":` - если 1
- `add_workout(conn)` - вызвать функцию №2
- `elif choice == "2":` - если 2
- `get_all_workouts(conn)` - вызвать функцию №3
- и так далее для всех цифр
- `elif choice == "0":` - если 0
- `break` - выйти из цикла
- `else:` - иначе (любая другая цифра)
- `print("Неправильно!")` - ошибка

---

## ПОСЛЕДНЯЯ СТРОКА:
```python
menu()
```
- Вызвать функцию №9 - запустить программу

---

## ИТОГ:
- **9 функций** в коде
- Каждая делает свою конкретную задачу
- Главная функция `menu()` вызывает остальные по выбору пользователя
