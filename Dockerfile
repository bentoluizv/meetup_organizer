FROM python:3.12.4-alpine

RUN python -m pip install --upgrade pip

RUN pip install poetry

WORKDIR /meetup_organizer

COPY . .

RUN poetry install -n --without dev

EXPOSE 8000

ENTRYPOINT [ "entrypoint.sh" ]
CMD ["sh"]