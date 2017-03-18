FROM python:3.5

MAINTAINER David Wyde (david.wyde@gmail.com)

# Install extra software
#RUN apt-get update

RUN pip3 install django pyyaml

# Add the user
RUN useradd --create-home scoreboard

# Set our working directory
WORKDIR /home/scoreboard

# Copy the app in
COPY . /home/scoreboard/
RUN chown -R scoreboard /home/scoreboard/challenges/migrations

# Switch users
USER scoreboard

RUN ./manage.py makemigrations
RUN ./manage.py migrate
RUN ./manage.py loaddata challenges

# Run the app
CMD ["./manage.py", "runserver", "0.0.0.0:9000"]
