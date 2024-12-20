# service_desk
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

### накатите миграцию
```bazaar
alembic upgrade head
```

### запустить приложение в папке app
```bazaar
python main.py
```

### swagger
```bazaar
http://127.0.0.1:8000/api/v1/service_desk/swagger
```