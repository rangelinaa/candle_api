# Candle Shop API

FastAPI + PostgreSQL в Docker.

    docker compose up --build

API: http://localhost:8000/docs
БД: localhost:5432, база candle_shop (таблицы создаются из migrations/001_init.sql)

API пока работает с данными в памяти, к БД не подключено.
