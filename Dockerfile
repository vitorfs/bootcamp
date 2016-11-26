FROM python:3.5
ENV PYTHONUNBUFFERED 1

ADD ./requirements.txt /requirements.txt
ADD ./entrypoint.sh /entrypoint.sh
ADD . /bootcamp

RUN pip install -r requirements.txt

RUN groupadd -r django && useradd -r -g django django

RUN chown -R django /bootcamp && chmod +x entrypoint.sh && chown django entrypoint.sh

WORKDIR /bootcamp

ENTRYPOINT ["/entrypoint.sh"]
