# Устанавливаем базовый образ для Python 3.11.3
FROM python:3.11.4-slim

# Устанавливаем рабочую директорию внутри контейнера


WORKDIR /app

# Копируем и устанавливаем requirements.txt
COPY requirements.txt .

RUN pip install -r requirements.txt

# Копируем файлы проекта в контейнер
COPY . .


# RUN chmod a+x ../docker/*.sh
# Запускаем миграции Alembic
# RUN alembic upgrade head

# # Команда для запуска FastAPI-приложения при старте контейнера
# CMD ["uvicorn", "main:app", "--env-file", "./venv", "--host", "0.0.0.0", "--port", "8000"]

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
# CMD uvicorn main:app --workers 4 --env-file venv --bind=0.0.0.0:8000