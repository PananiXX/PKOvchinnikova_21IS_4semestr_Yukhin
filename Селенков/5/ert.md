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
