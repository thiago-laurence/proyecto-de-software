FROM python:3.8-alpine

WORKDIR /code

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

RUN pip install poetry==1.6.1

COPY ./ ./

RUN poetry install

COPY entrypoint.sh ./entrypoint.sh

EXPOSE 5000

ENTRYPOINT [ "./entrypoint.sh" ]

# CMD ["poetry", "run", "flask", "run", "--debug", "--cert", "adhoc"]
CMD ["poetry", "run", "flask", "run", "--debug"]