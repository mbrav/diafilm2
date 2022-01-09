[![.github/workflows/pytest.yml](https://github.com/mbrav/diafilm2/actions/workflows/pytest.yml/badge.svg)](https://github.com/mbrav/diafilm2/actions/workflows/pytest.yml)
[![wakatime](https://wakatime.com/badge/user/54ad05ce-f39b-4fa3-9f2a-6fe4b1c53ba4/project/bc1260ce-04cd-47aa-a976-a2e3247fa31a.svg)](https://wakatime.com/badge/user/54ad05ce-f39b-4fa3-9f2a-6fe4b1c53ba4/project/bc1260ce-04cd-47aa-a976-a2e3247fa31a)

# diafilm2

«Δиа Фильм²» – это проект, который разрабатывался для курса Яндекс Практикум . Не исключено, что проект получит дальнейшее внимание и его развитие продолжится. На данный момент проект будет сохранен в том виде, в котором он сейчас находится.

## Instructions

```
$ git clone https://github.com/mbrav/diafilm2.git
$ cd diafilm2
```

Setup a local python environment:

```
$ python3 -m venv venv
$ source venv/bin/activate
```

Install dependencies:

```
$ pip3 install -r requirements.txt
```

Rename `dev.env` environment file to `.env`:

```
$ mv backend/diafilm/dev.env backend/diafilm/.env
```

Setup Django database and migrations:

```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

Setup an admin user:

```
$ python3 manage.py createsuperuser
```

Run server

```
$ python3 manage.py runserver
```

Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
