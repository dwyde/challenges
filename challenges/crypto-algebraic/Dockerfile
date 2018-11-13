FROM python:3.6

MAINTAINER David Wyde (david.wyde@gmail.com)

RUN pip3 install tornado

RUN useradd -m challenge

COPY server.py index.html puzzle.js style.css /home/challenge/
COPY chessboardjs /home/challenge/chessboardjs

WORKDIR /home/challenge

# Set permissions
RUN chown -R root:challenge server.py index.html puzzle.js style.css chessboardjs
RUN chmod 640 server.py index.html puzzle.js style.css
RUN find chessboardjs -type d -exec chmod 750 {} \;
RUN find chessboardjs -type f -exec chmod 640 {} \;

EXPOSE 8888

USER challenge

CMD ["python3", "server.py"]

