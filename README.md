# factories
Тестовое задание

#### Переменные окружения
Необходимо в папке ./src создать файл .env
Пример заполнения находиться в файле .env.example


Make docker-compose containers:
```shell
cd src
vim .env
cd ..
docker-compose up -d --build
```


### Prepare database
```
docker exec factory alembic revision --autogenerate -m "create inital tables"
docker exec factory alembic upgrade head
```

### Documentation
Visit OpenAPI web page:
```
http://127.0.0.1:8000/api/factories/openapi#/
```
