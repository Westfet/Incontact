FROM python:3.11.2

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


ENV APP_HOME=/in_contact
#RUN mkdir $APP_HOME
#RUN mkdir $APP_HOME/static
#RUN mkdir $APP_HOME/media

WORKDIR $APP_HOME

COPY ./requirements.txt /tmp/
COPY ./ /in_contact
RUN pip install -U pip
RUN pip install --upgrade setuptools
RUN pip install -r /tmp/requirements.txt


