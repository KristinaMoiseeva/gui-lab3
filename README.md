# Лабораторная работа №3 — PyQt5 + SQL

## Задание

Реализовать приложение на PyQt5 с использованием табличного представления и работы с SQL.

Программа должна:

- через меню устанавливать соединение с SQLite БД;
- через меню закрывать соединение и очищать результаты;
- после подключения выполнять `SELECT * FROM sqlite_master` и выводить результат в `Tab1`;
- по кнопке `bt1` выполнять `SELECT name FROM sqlite_master` и выводить результат в `Tab2`;
- через `QComboBox` выбирать колонку `sqlite_master`, выполнять соответствующий запрос и выводить результат в `Tab3`;
- по кнопкам `bt2` и `bt3` выполнять дополнительные SQL-запросы и выводить результаты в `Tab4` и `Tab5`.

## Реализованные элементы

### Menu → Set connection

Открывается `QFileDialog`, через который выбирается SQLite-файл (`*.db`, `*.sqlite`, `*.sqlite3`).

После успешного подключения автоматически выполняется:

```sql
SELECT * FROM sqlite_master;
```

Результат отображается в `Tab1`.

### Menu → Close connection

Соединение с БД закрывается, содержимое всех вкладок очищается, элементы управления блокируются до следующего подключения.

### bt1

Выполняется запрос:

```sql
SELECT name FROM sqlite_master;
```

Результат отображается в `Tab2`.

### QComboBox Columns

В список загружаются колонки `sqlite_master`:

```text
type
name
tbl_name
rootpage
sql
```

При выборе колонки выполняется запрос вида:

```sql
SELECT name FROM sqlite_master;
```

Результат отображается в `Tab3`.

### bt2 — Query2

```sql
SELECT type, COUNT(*) AS object_count
FROM sqlite_master
GROUP BY type
ORDER BY type;
```

Результат отображается в `Tab4`.

### bt3 — Query3

```sql
SELECT name, type, tbl_name, sql
FROM sqlite_master
ORDER BY name;
```

Результат отображается в `Tab5`.

## Используемые компоненты PyQt5

- `QMainWindow`
- `QMenuBar`
- `QAction`
- `QFileDialog`
- `QPushButton`
- `QComboBox`
- `QTabWidget`
- `QTableView`
- `QSqlDatabase`
- `QSqlQuery`
- `QSqlQueryModel`

## Структура проекта

```text
gui-lab3/
├── main.py
├── sample.db
├── README.md
├── requirements.txt
└── .gitignore
```

`sample.db` — тестовая SQLite-база, которая входит в проект. Её можно выбрать через `Menu → Set connection`.

## Установка на Windows

Скачайте репозиторий через **Code → Download ZIP**, распакуйте его и перейдите в папку проекта.

Например:

```powershell
cd "$HOME\Downloads\gui-lab3-main"
```

Проверьте содержимое:

```powershell
dir
```

Должны быть:

```text
main.py
sample.db
README.md
requirements.txt
```

Создайте виртуальное окружение:

```powershell
python -m venv .venv
```

Установите зависимости:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Запуск

```powershell
.\.venv\Scripts\python.exe main.py
```

## Проверка лабораторной

1. Запустите приложение.
2. Выберите **Menu → Set connection**.
3. Выберите `sample.db`.
4. Убедитесь, что в `Tab1` появилась таблица `sqlite_master`.
5. Нажмите `bt1` — результат появится в `Tab2`.
6. Выберите колонку в `QComboBox` — результат появится в `Tab3`.
7. Нажмите `bt2` — результат появится в `Tab4`.
8. Нажмите `bt3` — результат появится в `Tab5`.
9. Выберите **Menu → Close connection** — все таблицы очистятся.
