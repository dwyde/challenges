FROM ubuntu

MAINTAINER David Wyde (david.wyde@gmail.com)

# Install extra software
RUN apt update
RUN apt install -y python3-pip nginx nginx-extras sudo
RUN pip3 install django==2.2 pyyaml psycopg2-binary uwsgi
RUN apt remove -y python3-pip

# Add the user
RUN useradd --create-home scoreboard
RUN usermod -a -G scoreboard www-data

# Set our working directory
WORKDIR /home/scoreboard

# Copy the app in
COPY . /home/scoreboard/

# Hack to allow recent Postgres to start: no root password
ENV POSTGRES_HOST_AUTH_METHOD trust

# Move nginx cert and key
RUN mv under-the-ctf.* /etc/nginx
RUN chown www-data:root /etc/nginx/under-the-ctf.*
RUN chmod 440 /etc/nginx/under-the-ctf.*

# Allow the scoreboard user to write files
RUN chown -R scoreboard challenges/migrations/
RUN touch debug.log
RUN chown scoreboard debug.log

# Allow Django to read and write secrets
RUN mkdir /secrets
RUN chown -R scoreboard:scoreboard /secrets
RUN chmod -R 700 /secrets

# Deploy the nginx configuration
RUN cp /home/scoreboard/nginx.conf /etc/nginx/sites-enabled/default
RUN cp /home/scoreboard/sudoers /etc/sudoers

# Switch users
USER scoreboard

# Run the app as the 'scoreboard' user
CMD sudo /usr/sbin/service nginx start && ./run.sh

