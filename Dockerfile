FROM python:3.8

WORKDIR /conveyeer

COPY . /conveyeer

RUN apt update -y && apt install -y redis-server

RUN chmod u+x pictor/font_setup.sh && pictor/font_setup.sh

RUN pip install -r requirements.txt

RUN chmod +x ./start_all_services.sh

ENTRYPOINT ["./start_all_services.sh"]