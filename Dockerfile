FROM python:3.12.4

RUN pip install poetry

WORKDIR /meetup_organizer

COPY . .

RUN poetry lock
RUN poetry install

EXPOSE 8000

CMD ["poetry","run", "fastapi", "run", "meetup_organizer/app.py"]