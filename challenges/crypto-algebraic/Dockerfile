FROM python:3.5

MAINTAINER David Wyde (david.wyde@gmail.com)

RUN pip3 install tornado

RUN useradd -m challenge

COPY server.py index.html puzzle.js style.css /home/challenge/
COPY chessboardjs /home/challenge/chessboardjs

EXPOSE 8888

USER challenge

WORKDIR /home/challenge

CMD ["python3", "server.py"]
