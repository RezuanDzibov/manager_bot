FROM python:3

ENV APP_HOME=/home/app
ENV WEB_HOME=/home/app/web

RUN mkdir -p $APP_HOME
RUN mkdir -p $WEB_HOME


WORKDIR $APP_HOME

RUN apt update && apt install python3 netcat -y

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . $WEB_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
COPY ./media/* $APP_HOME/mediafiles

RUN pip install -r $WEB_HOME/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:${WEB_HOME}"

RUN chmod +x /home/app/web/entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]