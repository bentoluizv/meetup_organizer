FROM python:3.12.4

RUN pip install poetry

WORKDIR /app

COPY . .

RUN poetry lock
RUN poetry install

CMD ["poetry","run", "fastapi", "run", "meetup_organizer/app.py"]