# Замечания 

- Неправильно сгруппированы импорты. Посмотри, как это рекомендуется делать в pep8 (порядок групп, разделение пустыми строками и т.д.) Еще можно использовать библиотеку `isort`. Вот есть [статья по настройке](https://simpleisbetterthancomplex.com/packages/2016/10/08/isort.html). Стоит проверить и поправить по всему проекту
    - `isort . --recursive --check-only`
    - `isort . --recursive`

To dump data:
`python manage.py dumpdata app.model_name --indent 4 > fixtures/file_name.json`

To load data:
`python manage.py loaddata fixtures/model_name.json --app app.model_name`

### thumbnail cleanup

- `python manage.py thumbnail cleanup && python manage.py thumbnail clear && python manage.py thumbnail clear_delete_referenced && python manage.py thumbnail clear_delete_all`