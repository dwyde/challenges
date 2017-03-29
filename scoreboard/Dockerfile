FROM python:3.5

MAINTAINER David Wyde (david.wyde@gmail.com)

# Install extra software
#RUN apt-get update

RUN pip3 install django pyyaml psycopg2

# Add the user
RUN useradd --create-home scoreboard

# Set our working directory
WORKDIR /home/scoreboard

# Copy the app in
COPY . /home/scoreboard/
RUN chown -R scoreboard /home/scoreboard/challenges/migrations

# Switch users
USER scoreboard

# Run the app
CMD ./run.sh
