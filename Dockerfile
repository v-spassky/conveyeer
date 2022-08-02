FROM python:3.8

WORKDIR /conveyeer

COPY * .

RUN apt install redis-server

RUN chmod u+x pictor/font_setup.sh && pictor/font_setup.sh

RUN pip install -r requirements.txt

RUN ./start_all_services.sh

EXPOSE 8000