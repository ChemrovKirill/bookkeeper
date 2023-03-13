# Простая программа для управления личными финансами
#### (учебный проект для курса по практике программирования на Python)

### От разработчика
Для запуска приложения:
```commandline
poetry run python bookkeeper
```
Функциональность:
- изменение бюджета производится в главном окне по двойному клику
- удаление бюджета происходит при пустом поле "Бюджет"
- добавление записи о расходе производится в главном окне
- изменение записей о расходе производится в таблице по двойному клику
- удаление записей о расходе производится по нажатию на кнопку 
"удалить выбранные расходы", при этом удаляются выделенные в таблице записи
- изменение списка категорий производится в отдельном окне по кнопке "Редактировать"
- категории для измененния можно выбирать из выпадающего списка, печать в поле 
или выбирать двойным кликом из древовидного списка категорий
- при удалении категории, все траты переходят в родительскую категорию или остаются без категории

При необходимости создания новой базы данных с нужными таблицами
можно использовать скрипт create_db_table.py:
```commandline
poetry run python create_db_table.py
```


[Техническое задание](specification.md)

Архитектура проекта строится на принципе инверсии зависимостей. Упрощенная схема
классов выглядит так:
![](structure.png)

Для хранения данных используется паттерн Репозиторий. Структура файлов
и каталогов (модулей и пакетов) отражает архитектуру:

📁 bookkeeper - исполняемый код 

- 📁 models - модели данных

    - 📄 budget.py - бюджет
    - 📄 category.py - категория расходов
    - 📄 expense.py - расходная операция
- 📁 repository - репозиторий для хранения данных

    - 📄 abstract_repository.py - описание интерфейса
    - 📄 memory_repository.py - репозиторий для хранения в оперативной памяти
    - 📄 sqlite_repository.py - репозиторий для хранения в sqlite (пока не написан)
- 📁 view - графический интерфейс (пока не написан)
- 📄 simple_client.py - простая консольная утилита, позволяющая посмотреть на работу программы в действии
- 📄 utils.py - вспомогательные функции

📁 tests - тесты (структура каталога дублирует структуру bookkeeper)

Для работы с проектом нужно сделать fork и склонировать его себе на компьютер.

Проект создан с помощью poetry. Убедитесь, что poetry у вас установлена
(инструкцию по установке можно посмотреть [здесь](https://python-poetry.org/docs/)).
Для установки всех зависимостей, запустите (убедитесь, что вы находитесь
в корневой папке проекта - там, где лежит файл pyproject.toml):

```commandline
poetry install
```

Для запуска тестов и статических анализаторов используйте следующие команды (убедитесь, 
что вы находитесь в корневой папке проекта):
```commandline
poetry run pytest --cov --cov-report term-missing
poetry run python -m pytest
poetry run mypy --strict bookkeeper
poetry run pylint bookkeeper
poetry run flake8 bookkeeper
poetry run flake8 --max-complexity 10
```

При проверке работы будут использоваться эти же инструменты с теми же настройками.

Задача первого этапа:
1. Сделать fork репозитория и склонировать его себе на компьютер
2. Написать класс SqliteRepository
3. Написать тесты к этому классу
4. Подключить СУБД sqlite к simple_client (пока он работает в оперативной памяти и все забывает при выходе)

Задача второго этапа:
1. Создать виджеты:
   - для отображения списка расходов с возможностью редактирования
   - для отображения бюджета на день/неделю/месяц с возможностью редактирования
   - для добавления нового расхода
   - для просмотра и редактирования списка категорий
2. Собрать виджеты в главное окно

В итоге окно должно выглядеть примерно так:

![](screenshot.png)

Воспроизводить данный дизайн в точности не требуется, вы можете использовать другие
виджеты, другую раскладку. Дизайн, представленный на скриншоте, предполагает, что 
редактирование списка категорий будет выполняться в отдельном окне. Вы можете
сделать так же, а можете все разместить в одном окне, использовать вкладки
или контекстные меню. Важно только реализовать функциональность.

Задачей этого этапа не является подключение реальной логики приложения и базы
данных. Пока нужно только собрать интерфейс. Файлы, описывающие интерфейс,
должны располагаться в папке bookkeeper/view.

Задача 3 этапа:
1. Написать тесты для графического интерфейса
2. Создать реализацию компонента Presenter модели MVP, тем самым соединив все компоненты
в работающее приложение.

Итогом 3 этапа должно быть полностью работающее приложение, реализующее всю требуемую
функциональность.

Задача 4 этапа:
1. Доделать, отдалить и привести в порядок все, что было сделано на предыдущих этапах
2. Добавить стилизацию (не влияет на оценку).
3. Добавить дополнительные функции (не влияет на оценку). Например:
    - возможность задать бюджет на день с переносом остатка на следующий день
    - формирование отчета за произвольный период
    - интерактивная визуализация данных в отчете
    - возможность добавления чека по qr-коду или скану
    - и т.д.

Реализация дополнительных функций и стилизация приложения не влияют на оценку, поэтому
сосредоточиться следует на том, чтобы основная функциональность хорошо работала
и код был хорошо написан.

Для сдачи работы достаточно прислать ссылку на свой форк в форму "Добавить ответ на задание" в ЛМС, 
pull-request создавать не надо.
