FROM python:3.5

MAINTAINER David Wyde (david.wyde@gmail.com)

RUN useradd -m challenge

COPY sql_injection.py /home/challenge/

USER challenge

WORKDIR /home/challenge

ENV PORT 8888

CMD ["python3", "sql_injection.py"]
