FROM python:3

ENV APP_HOME=/home/app
ENV BOT_HOME=/home/app/bot
ARG USER_PASSWORD

RUN mkdir -p $APP_HOME
RUN mkdir -p $BOT_HOME

RUN groupadd bot
RUN useradd -m -g bot bot -p $USER_PASSWORD
RUN usermod -aG bot bot

WORKDIR $APP_HOME

RUN apt update && apt install python3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . $BOT_HOME
RUN mkdir $APP_HOME/mediafiles

RUN pip install -r $BOT_HOME/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:${BOT_HOME}"
