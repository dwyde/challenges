FROM python:3.5

MAINTAINER David Wyde (david.wyde@gmail.com)

RUN pip3 install tornado

RUN useradd -m challenge

COPY sql_injection.py /home/challenge/

USER challenge

WORKDIR /home/challenge

CMD ["python3", "sql_injection.py"]

