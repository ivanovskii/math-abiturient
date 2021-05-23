FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh

COPY . . 

ENV DJANGO_SUPERUSER_PASSWORD=123456
ENV DJANGO_SUPERUSER_EMAIL=example@example.com
ENV DJANGO_SUPERUSER_USERNAME=admin

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]