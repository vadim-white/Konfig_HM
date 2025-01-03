# Конфигурационное управление
## Задание 2
### Вариант 15
Разработать инструмент командной строки для визуализации графа
зависимостей, включая транзитивные зависимости. Сторонние средства для
получения зависимостей использовать нельзя.
Зависимости определяются для git-репозитория. Для описания графа
зависимостей используется представление Mermaid. Визуализатор должен
выводить результат в виде сообщения об успешном выполнении и сохранять граф
в файле формата png.
Построить граф зависимостей для коммитов, в узлах которого содержатся
хеш-значения. Граф необходимо строить для ветки с заданным именем.
Ключами командной строки задаются:
- Путь к программе для визуализации графов.
- Путь к анализируемому репозиторию.
- Путь к файлу с изображением графа зависимостей.
- Имя ветки в репозитории.
Все функции визуализатора зависимостей должны быть покрыты тестами.

### Стек технологий
1.	Python 3: Основной язык программирования для реализации логики скрипта.
2.	Mermaid: используется для генерации визуальных графов зависимостей.
3.	argparse: Для обработки аргументов командной строки.
4.	git: система контроля версий, анализируемая скриптом.

### Описание функционала
- Построение графа зависимостей для коммитов в git-репозитории, включая транзитивные зависимости между ними.
- Визуализация графа зависимостей с использованием программы Mermaid.
- Вывод результата в виде графического файла формата PNG.
- Возможность указания пути к git-репозиторию, имени ветки и выходного файла для сохранения графа.
- Проверка корректности работы всех функций через набор тестов с использованием библиотеки unittest.

### Реализация
1.	Парсинг коммитов и веток:
  
     - Реализована функция get_branch_commits, которая извлекает список коммитов для заданной ветки в git-репозитории.
     - Реализована функция get_commit_parents, которая находит родительские коммиты для каждого указанного коммита.

2.	Построение графа зависимостей:

     - Реализована рекурсивная функция build_dependency_graph, которая создает полный граф зависимостей между коммитами, включая транзитивные зависимости, по хешам коммитов.
3.	Визуализация графа:

     - Реализована функция visualize_dependencies, которая создает графическое представление графа зависимостей в формате PNG, используя программу Mermaid.
     - Граф строится с учётом зависимостей между коммитами и выводится в файл, указанный пользователем.


