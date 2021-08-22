FROM python:3.7

LABEL desc="Splitwise dockerfile created by Hardik dadhich (dadhichhardik26@gmail.com)" 

RUN pip install fastapi uvicorn

EXPOSE 8000

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]