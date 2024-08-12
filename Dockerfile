FROM python:3.12.4

RUN python -m pip install --upgrade pip

RUN pip install poetry

WORKDIR /meetup_organizer

COPY . .

RUN poetry install -n --without dev

EXPOSE 8000

CMD ["poetry","run", "fastapi", "run", "./meetup_organizer/app.py"]