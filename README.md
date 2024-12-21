# Описание проекта service desk
приложение ServiceDesk работает с пользовательскими обращениями, фиксирует их в базе данных, с возможностью принятия этих
обращений сотрудниками поддержки.

#### stack: Python, FastAPI, SqlAlchemy, Pydantic, PostgreSQL, asyncsio, Alembic
### клонируем из гитхаба
```bazaar
ssh: git clone git@github.com:vawy/service_desk.git
```

### переходим в папку с проектом
### создаем виртуальное окружение, активируем, устанавливаем зависимости
Для Linux/MacOs
```bazaar
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### устанавливаем докер для постгреса
https://docs.docker.com/desktop/

### поднять в докере постгрес
```
docker run --name my_postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=test_db -p 5432:5432 -d postgres:latest
```

#### после создайте в app/settings файл .env, куда поместите данные о бд
```bazaar
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=test_db
```

### перейдите в корень проекта и накатите миграцию
```bazaar
alembic upgrade head
```

### запустить приложение из папки app
```bazaar
python main.py
```

### swagger
```bazaar
http://127.0.0.1:8000/api/v1/service_desk/swagger
```
