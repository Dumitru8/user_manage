FROM python:3.11-alpine3.18

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /user_manage

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN chmod a+x /user_manage/entrypoint.sh
